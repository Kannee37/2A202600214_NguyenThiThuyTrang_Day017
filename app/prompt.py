def build_prompt(state):
    return f"""
You are a helpful multi-memory agent.

[USER PROFILE MEMORY]
{state["user_profile"]}

[EPISODIC MEMORY]
{state["episodes"]}

[SEMANTIC MEMORY]
{state["semantic_hits"]}

[RECENT CONVERSATION]
{state["recent_conversation"]}

[CURRENT USER QUERY]
{state["query"]}

Answer using relevant memory only. If memory conflicts, prefer the latest updated profile fact.
"""