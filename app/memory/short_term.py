class ConversationBufferMemory:
    """
    Short-term memory:
    Lưu các message gần nhất trong session hiện tại.
    """

    def __init__(self, max_messages: int = 6):
        self.max_messages = max_messages
        self.messages = []

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self.messages = self.messages[-self.max_messages:]

    def get(self):
        return self.messages

    def clear(self):
        self.messages = []