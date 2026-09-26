# Prompt Log

**AI tool used:** Claude Code (CLI), model Claude Opus 5.5 (Anthropic)
**Chatbot model:** OpenAI GPT API (called from the backend; key stored on Render, not in this repo)

Key prompts that shaped this project, in order, with a short note on what the AI did in response.

---

## Session 1 — 2026-09-26

### 1. Choosing a project
> *(Pasted the assignment description and requirements)* "Can you suggest some use cases of where I can use Render to make my website better"

Claude looked at my existing portfolio (`VedaantK.github.io`) and NBA Predictor repo and suggested
five backend ideas tailored to them: a live NBA Predictor API, a Road Racer global leaderboard,
a "Chat with Vedaant" AI chatbot, a working contact form, and a visitor guestbook.

### 2. Picking the chatbot and building a persona questionnaire
> "I think the chatbot with me would be cool, ask me as many targeted questions as you can in a md file that will help you train a GPT wrapper, which I have 10 dollars of credit for to talk as similar to me as possible."

Claude created `persona_questions.md` with 62 questions across 7 parts (voice samples, texting
style, background, projects, interests, personality, bot rules). It pre-filled facts already on my
portfolio and explained that the bot will use a **system prompt** rather than fine-tuning, which is
cheaper and fits within the $10 budget.

### 3. Cleaning up my answers
> "Ok, I have answered a lot of the questions, can you clean up a lot of my answers first. Fix things like typos and other things"

Claude fixed spelling, grammar, and capitalization in the factual sections, but intentionally left
the casual style of my voice samples (missing apostrophes, slang) alone so the bot still sounds like
me. It also flagged factual issues (e.g. swing trading isn't "long term", a restaurant name, an
answer placed under the wrong question) and listed the most important unanswered questions.

### 4. Corrections
> "for q5 change it back to swing trading and fix the other things, yeah q6 is right, i have done a few v6's. Hell is fine."

Claude applied my corrections to the stock market answer, climbing grade, and swearing rule.

### 5. Final answers + prompt log
> "Ok, everything is working and saved now. Also remember to keep a prompt log for all our conversations we have talked about"

Claude cleaned up my new answers (including the bot's rules: deflect personal topics, admit being an
AI, point people to my email, keep replies short) and created this prompt log.

### 6. Wrapping up
> "if everything is good for now I am going to exit this chat and do my Render Integration"

Claude gave a Render deployment checklist: keep the OpenAI key in Render environment variables and
out of git, use gunicorn, allow CORS from my GitHub Pages domain, keep costs low, show a message
while the free tier wakes up, and handle errors on the frontend.

### 7. Committing
> "Make sure everything is committed. the prompt log should only be this convo."

Claude initialized this repo with a `.gitignore` (so `.env` files with API keys can never be
committed) and committed the questionnaire and this log.
