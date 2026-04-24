def extract_profile_update(query: str):
    q = query.lower()

    if "tôi thích dùng fastapi" in q:
        return {"backend_preference": "FastAPI"}

    if "tôi muốn code tách từng file" in q:
        return {"code_style": "split_files"}

    if "tôi dị ứng sữa bò" in q:
        return {"allergy": "sữa bò"}

    if "dị ứng đậu nành" in q and "không phải sữa bò" in q:
        return {"allergy": "đậu nành"}

    return {}