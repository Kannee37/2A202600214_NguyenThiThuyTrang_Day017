import json


class SemanticMemory:
    """
    Semantic memory:
    Lưu knowledge/fact/rule dùng chung.
    """

    def __init__(self, path="app/data/semantic_docs.json"):
        self.path = path

    def load_docs(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def search(self, query: str):
        docs = self.load_docs()
        results = []

        for doc in docs:
            text = doc["title"] + " " + doc["content"]
            if query.lower() in text.lower():
                results.append(doc)

        return results[:3]