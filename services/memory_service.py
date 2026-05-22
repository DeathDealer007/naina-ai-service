from typing import List, Dict
import time

class MemoryService:
    def __init__(self, max_history_len: int = 12, expiry_seconds: int = 3600):
        # session_id -> list of message dicts
        self.sessions: Dict[str, List[Dict[str, str]]] = {}
        # session_id -> last active timestamp (for cleanup)
        self.last_active: Dict[str, float] = {}
        self.max_history_len = max_history_len
        self.expiry_seconds = expiry_seconds

    def _cleanup_expired_sessions(self):
        now = time.time()
        expired = [
            sid for sid, active_time in self.last_active.items()
            if now - active_time > self.expiry_seconds
        ]
        for sid in expired:
            if sid in self.sessions:
                del self.sessions[sid]
            if sid in self.last_active:
                del self.last_active[sid]

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        self._cleanup_expired_sessions()
        self.last_active[session_id] = time.time()
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]

    def add_message(self, session_id: str, role: str, content: str):
        self._cleanup_expired_sessions()
        self.last_active[session_id] = time.time()
        
        if session_id not in self.sessions:
            self.sessions[session_id] = []
            
        self.sessions[session_id].append({"role": role, "content": content})
        
        # Cap the history length (keeping system prompt rules separate or relying on SDK parameters)
        if len(self.sessions[session_id]) > self.max_history_len:
            # Maintain even length to keep user-model pairs intact if possible, or just slice
            self.sessions[session_id] = self.sessions[session_id][-self.max_history_len:]

    def clear_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.last_active:
            del self.last_active[session_id]
            
# Create a singleton instance to be shared across requests
memory_db = MemoryService()
