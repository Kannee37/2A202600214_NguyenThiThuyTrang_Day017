from app.utils.token_counter import estimate_tokens


class ContextWindowManager:
    """
    Quản lý context window.
    Ưu tiên giữ:
    1. System instruction
    2. User task hiện tại
    3. Long-term / semantic memory
    4. Short-term history
    """

    def __init__(self, token_limit: int = 2500):
        self.token_limit = token_limit

    def trim(self, context_items):
        total = 0
        selected = []

        priority_order = {
            "system": 1,
            "task": 2,
            "memory": 3,
            "history": 4
        }

        sorted_items = sorted(
            context_items,
            key=lambda x: priority_order.get(x["type"], 99)
        )

        for item in sorted_items:
            tokens = estimate_tokens(item["content"])
            if total + tokens <= self.token_limit:
                selected.append(item)
                total += tokens

        return selected