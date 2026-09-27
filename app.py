import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel

SYSTEM_PROMPT = Path(__file__).parent.joinpath("system_prompt.md").read_text()
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("ALLOWED_ORIGINS", "https://vedaantk.github.io").split(",")
    if origin.strip()
]
MAX_HISTORY_MESSAGES = 10

# Reads OPENAI_API_KEY from the environment automatically.
client = OpenAI()

app = FastAPI(title="Vedaant.EXE Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class HistoryMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[HistoryMessage] = []


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="message cannot be empty")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for h in req.history[-MAX_HISTORY_MESSAGES:]:
        if h.role in ("user", "assistant"):
            messages.append({"role": h.role, "content": h.content})
    messages.append({"role": "user", "content": message})

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=300,
            temperature=0.9,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"upstream chat error: {exc}") from exc

    return ChatResponse(reply=completion.choices[0].message.content)
