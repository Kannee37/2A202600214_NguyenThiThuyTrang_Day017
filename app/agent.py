from app.memory.short_term import ConversationBufferMemory
from app.memory.long_term import RedisLongTermMemory
from app.memory.episodic import EpisodicMemory
from app.memory.semantic import SemanticMemory
from app.memory.router import MemoryRouter
from app.utils.context_manager import ContextWindowManager


class MultiMemoryAgent:
    def __init__(self):
        self.short_term = ConversationBufferMemory()
        self.long_term = RedisLongTermMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
        self.router = MemoryRouter()
        self.context_manager = ContextWindowManager()

    def build_context(self, user_id: str, query: str):
        memory_type = self.router.route(query)

        context_items = [
            {
                "type": "system",
                "content": "You are a helpful multi-memory AI agent."
            },
            {
                "type": "task",
                "content": query
            }
        ]

        if memory_type == "long_term":
            user_memory = self.long_term.get_user_memory(user_id)
            context_items.append({
                "type": "memory",
                "content": f"User preferences: {user_memory}"
            })

        elif memory_type == "episodic":
            events = self.episodic.search_events(user_id, query)
            context_items.append({
                "type": "memory",
                "content": f"Past user events: {events}"
            })

        elif memory_type == "semantic":
            docs = self.semantic.search(query)
            context_items.append({
                "type": "memory",
                "content": f"Relevant knowledge: {docs}"
            })

        history = self.short_term.get()
        context_items.append({
            "type": "history",
            "content": str(history)
        })

        trimmed = self.context_manager.trim(context_items)
        return trimmed, memory_type

    def respond(self, user_id: str, query: str):
        self.short_term.add("user", query)

        context, memory_type = self.build_context(user_id, query)

        response = (
            f"[Memory used: {memory_type}]\n"
            f"Agent response based on context:\n"
            f"{context}"
        )

        self.short_term.add("assistant", response)

        return {
            "query": query,
            "memory_used": memory_type,
            "response": response,
            "context_used": context
        }