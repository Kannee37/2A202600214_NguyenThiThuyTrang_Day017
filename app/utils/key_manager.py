import os
from dotenv import load_dotenv

load_dotenv()


class GeminiKeyManager:
    def __init__(self):
        keys = os.getenv("GEMINI_API_KEYS", "")
        self.keys = [k.strip() for k in keys.split(",") if k.strip()]
        self.index = 0

    def get_current_key(self):
        if not self.keys:
            raise ValueError("No API keys found")
        return self.keys[self.index]

    def rotate_key(self):
        self.index += 1
        if self.index >= len(self.keys):
            raise Exception("⛔ Hết tất cả API keys")
        return self.get_current_key()