from typing import TypedDict, List, Dict, Any


class MemoryState(TypedDict):
    user_id: str
    query: str
    messages: List[Dict[str, str]]

    user_profile: Dict[str, Any]
    episodes: List[Dict[str, Any]]
    semantic_hits: List[Dict[str, str]]
    recent_conversation: List[Dict[str, str]]

    memory_budget: int
    memory_used: str
    prompt: str
    response: str