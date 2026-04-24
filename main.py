from app.graph import build_graph


def run_demo():
    graph = build_graph()
    user_id = "user_001"

    conversations = [
        {
            "title": "Long-term preference",
            "turns": [
                "Tôi thích dùng FastAPI",
                "Lần sau tạo backend thì bạn nhớ dùng gì?",
                "FastAPI là gì?"
            ]
        },
        {
            "title": "Conflict update",
            "turns": [
                "Tôi dị ứng sữa bò",
                "À nhầm, tôi dị ứng đậu nành chứ không phải sữa bò",
                "Tôi dị ứng gì?"
            ]
        },
        {
            "title": "Episodic memory",
            "turns": [
                "Tôi bị lỗi CSS @import trong Next.js",
                "Tôi đã từng gặp lỗi này chưa?",
                "Rule của @import là gì?"
            ]
        }
    ]

    for conv in conversations:
        print("\n" + "=" * 50)
        print(f"SCENARIO: {conv['title']}")
        print("=" * 50)

        for turn in conv["turns"]:
            print(f"\nUser: {turn}")

            result = graph.invoke({
                "user_id": user_id,
                "query": turn,
                "messages": [],
                "user_profile": {},
                "episodes": [],
                "semantic_hits": [],
                "recent_conversation": [],
                "memory_budget": 2500,
                "prompt": "",
                "response": ""
            })

            print("\nAssistant:")
            print(result["response"])


if __name__ == "__main__":
    run_demo()