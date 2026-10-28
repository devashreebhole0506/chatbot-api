# Chatbot API

A small FastAPI chat app with an OpenAI-backed assistant, browser UI, and per-session conversation history.

## Run locally

From this directory, create and activate a virtual environment, install dependencies, and configure the API key:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `OPENAI_API_KEY` in `.env`. `OPENAI_MODEL` defaults to `gpt-4.1-mini`; `APP_NAME` controls the service title. Start the server with:

```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/` to chat, or `http://127.0.0.1:8000/docs` for the API reference. `POST /chat` accepts an optional `session_id` and a message. If omitted, the API creates a session ID and returns it with the reply. `DELETE /sessions/{session_id}` clears that session's history.

## Notes

- The API key is only needed when sending a chat message; the app and health route can start without it.
- Conversation history is held in process memory, capped at 40 messages by default, and cleared when the server restarts. Set `MAX_HISTORY_MESSAGES` to change the cap.
- For a multi-worker or production deployment, replace in-memory history with shared persistent storage and configure appropriate authentication and rate limits.
