import json
from app.graph import build_graph


def make_initial_state(user_id: str, query: str):
    return {
        "user_id": user_id,
        "query": query,
        "messages": [],
        "user_profile": {},
        "episodes": [],
        "semantic_hits": [],
        "recent_conversation": [],
        "memory_budget": 2500,
        "memory_used": "",
        "prompt": "",
        "response": ""
    }


def run_benchmark():
    graph = build_graph()

    with open("app/data/benchmark_conversations.json", "r", encoding="utf-8-sig") as f:
        conversations = json.load(f)

    results = []

    for conv in conversations:
        user_id = f"user_{conv['id']}"

        for turn_index, turn in enumerate(conv["turns"], start=1):
            output = graph.invoke(make_initial_state(user_id, turn))

            results.append({
                "conversation_id": conv["id"],
                "turn_index": turn_index,
                "query": turn,
                "memory_used": output.get("memory_used", "unknown"),
                "response_length": len(output.get("response", "")),
                "response": output.get("response", "")
            })

    with open("reports/benchmark_results.json", "w", encoding="utf-8-sig") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Benchmark completed.")
    print("Saved to reports/benchmark_results.json")


if __name__ == "__main__":
    run_benchmark()