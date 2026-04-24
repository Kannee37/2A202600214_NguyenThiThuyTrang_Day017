import json
import os


class LongTermProfileMemory:
    def __init__(self, path="app/data/profile_memory.json"):
        self.path = path
        if not os.path.exists(self.path):
            self._save({})

    def _load(self):
        with open(self.path, "r", encoding="utf-8-sig") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.path, "w", encoding="utf-8-sig") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def update_profile(self, user_id: str, updates: dict):
        data = self._load()
        data.setdefault(user_id, {})

        for key, value in updates.items():
            data[user_id][key] = value

        self._save(data)

    def get_profile(self, user_id: str):
        return self._load().get(user_id, {})