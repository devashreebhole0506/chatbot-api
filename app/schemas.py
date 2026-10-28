from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str | None = Field(default=None, min_length=1, max_length=128)
    message: str = Field(min_length=1, max_length=5000)


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    status: str = "success"


class HealthResponse(BaseModel):
    status: str
    service: str
    model_configured: bool
