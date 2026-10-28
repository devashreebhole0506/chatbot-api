from collections import defaultdict
from threading import Lock, RLock


class ConversationMemory:
    def __init__(self, max_messages: int = 40):
        self._history = defaultdict(list)
        self._lock = Lock()
        self._session_locks = defaultdict(RLock)
        # Keep complete user/assistant exchanges when trimming history.
        self._max_messages = max(2, max_messages - (max_messages % 2))

    def session_lock(self, session_id: str) -> RLock:
        with self._lock:
            return self._session_locks[session_id]

    def get_history(self, session_id: str) -> list[dict]:
        with self._lock:
            return [dict(item) for item in self._history[session_id]]

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:
        with self._lock:
            self._history[session_id].append(
                {
                    "role": role,
                    "content": content,
                }
            )
            if len(self._history[session_id]) > self._max_messages:
                del self._history[session_id][:-self._max_messages]

    def clear(self, session_id: str) -> None:
        with self._lock:
            self._history.pop(session_id, None)


from app.config import settings

memory = ConversationMemory(settings.max_history_messages)
