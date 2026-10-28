from langchain_openai import ChatOpenAI

from app.config import settings


class LLMService:
    def __init__(self):
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured.")
        self.model = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0.3,
        )

    def generate_reply(
        self,
        message: str,
        history: list[dict],
    ) -> str:
        messages = [
            (
                "system",
                "You are a helpful AI assistant. "
                "Answer accurately and clearly. "
                "If you are uncertain, say so.",
            )
        ]

        for item in history:
            messages.append(
                (
                    item["role"],
                    item["content"],
                )
            )

        messages.append(("human", message))

        response = self.model.invoke(messages)
        content = response.content
        if isinstance(content, str):
            reply = content.strip()
        else:
            reply = "\n".join(
                str(part.get("text", ""))
                for part in content
                if isinstance(part, dict) and part.get("type") == "text"
            ).strip()
        if not reply:
            raise RuntimeError("The language model returned an empty response.")
        return reply
