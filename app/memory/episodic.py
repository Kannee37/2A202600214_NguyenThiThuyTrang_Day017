import json
import os
from datetime import datetime


class EpisodicMemory:
    """
    Episodic memory:
    Lưu các trải nghiệm/sự kiện đã xảy ra với user.
    """

    def __init__(self, path="app/data/episodic_log.json"):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8-sig") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _load(self):
        with open(self.path, "r", encoding="utf-8-sig") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.path, "w", encoding="utf-8-sig") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_event(self, user_id: str, event: str, solution: str = ""):
        data = self._load()
        data.append({
            "user_id": user_id,
            "event": event,
            "solution": solution,
            "timestamp": datetime.now().isoformat()
        })
        self._save(data)

    def search_events(self, user_id: str, query: str):
        data = self._load()
        results = []

        for item in data:
            if item["user_id"] == user_id:
                text = item["event"] + " " + item.get("solution", "")
                if query.lower() in text.lower():
                    results.append(item)

        return results[-3:]