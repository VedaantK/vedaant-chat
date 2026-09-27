# Vedaant.EXE — Chat Backend

## What is this?

I made a chatbot trained to talk like me, so visitors on my portfolio can ask it questions and
get answers in roughly my own voice instead of a generic AI response. I had Claude write me a
questionnaire covering everything from how I actually text to my background, projects, and
opinions, and I answered it. That became the persona the bot uses. I then connected the OpenAI
API to my portfolio site through a backend deployed on Render, so the chatbot on the website can
actually talk to visitors.

This repo is just the backend — the FastAPI service that holds the persona and calls OpenAI. The
frontend chat widget itself lives in my portfolio repo ([VedaantK.github.io](https://github.com/VedaantK/VedaantK.github.io)).

## How it works

1. `persona_questions.md` — the raw questionnaire and my answers (voice samples, background,
   projects, opinions, bot rules). This is the source material.
2. `system_prompt.md` — those answers rewritten as instructions for the model: who I am, how I
   talk, and what topics the bot should deflect.
3. `app.py` — a small FastAPI app with two routes:
   - `GET /health` — used by Render to check the service is alive.
   - `POST /chat` — takes `{"message": "...", "history": [...]}`, prepends the system prompt and
     recent conversation history, calls the OpenAI Chat Completions API, and returns the reply.
4. The portfolio's chat widget calls `/chat` directly from the browser. CORS on the backend is
   locked to `https://vedaantk.github.io`, so only my site can call it.

## Project structure

| File | Purpose |
|---|---|
| `app.py` | FastAPI app — the `/chat` and `/health` endpoints |
| `system_prompt.md` | The persona, as fed to the model |
| `persona_questions.md` | The original questionnaire + my answers |
| `requirements.txt` | Python dependencies |
| `runtime.txt` | Pins the Python version Render builds with |
| `.env.example` | Documents the required environment variables (no real keys) |
| `prompt_log.md` | Log of the AI prompts used to build this project |

## Running it locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export OPENAI_API_KEY=sk-...          # your own key
export OPENAI_MODEL=gpt-4o-mini       # optional, this is the default
export ALLOWED_ORIGINS=http://localhost:3000   # optional, for local frontend testing

uvicorn app:app --reload --port 8000
```

Then `curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message":"yo"}'`.

## Deployment (Render)

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
- **Environment variables** (set in the Render dashboard, never committed):
  - `OPENAI_API_KEY` — required
  - `OPENAI_MODEL` — optional, defaults to `gpt-4o-mini`
  - `ALLOWED_ORIGINS` — optional, defaults to `https://vedaantk.github.io`

## AI usage

I used Claude Code throughout this project: it wrote the persona questionnaire based on my
existing portfolio, cleaned up my answers without flattening the casual voice samples, turned the
answers into the system prompt, and wrote the FastAPI backend after my first Render deploy failed
because the repo didn't actually have any backend code in it yet. Claude also smoke-tested the
server locally and against the live Render deployment (health check, a real chat exchange, and a
CORS check from my actual site's origin) before anything got pushed. Every prompt that shaped this
project is in `prompt_log.md`.

## Known limitations

- Render's free tier spins the service down when idle, so the first message after a while can
  take up to ~30 seconds to respond. The frontend widget shows a message about this instead of
  just failing silently.
- The persona (`system_prompt.md`) is what visitors' messages get checked against, and it's
  public — anyone could ask the bot to repeat parts of it. Nothing sensitive is in there on
  purpose.
- Running on a small OpenAI budget, so it defaults to `gpt-4o-mini` rather than a pricier model.
