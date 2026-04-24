class MemoryRouter:
    """
    Chọn memory phù hợp dựa vào intent của query.
    """

    def route(self, query: str):
        q = query.lower()

        if any(word in q for word in ["tôi thích", "preference", "từ giờ", "luôn dùng"]):
            return "long_term"

        if any(word in q for word in ["trước đây", "đã từng", "lần trước", "hôm qua"]):
            return "episodic"

        if any(word in q for word in ["là gì", "rule", "khái niệm", "giải thích"]):
            return "semantic"

        return "short_term"