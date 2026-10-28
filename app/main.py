from uuid import uuid4
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.llm_service import LLMService
from app.memory import memory
from app.schemas import ChatRequest, ChatResponse, HealthResponse


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Session-based conversational chatbot API",
)

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

llm_service: LLMService | None = None


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        model_configured=bool(settings.openai_api_key),
    )


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    global llm_service
    session_id = request.session_id or str(uuid4())
    with memory.session_lock(session_id):
        history = memory.get_history(session_id)
        try:
            if llm_service is None:
                llm_service = LLMService()
            reply = llm_service.generate_reply(request.message, history)
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail="The language model request failed. Check the server configuration and try again.",
            ) from exc

        memory.add_message(session_id, "human", request.message)
        memory.add_message(session_id, "ai", reply)

    return ChatResponse(
        session_id=session_id,
        reply=reply,
    )


@app.delete("/sessions/{session_id}", status_code=204)
def clear_session(session_id: str):
    with memory.session_lock(session_id):
        memory.clear(session_id)
