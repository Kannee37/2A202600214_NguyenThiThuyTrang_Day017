import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from langgraph.graph import StateGraph, END

from app.state import MemoryState
from app.prompt import build_prompt
from app.memory.short_term import ConversationBufferMemory
from app.memory.long_term import LongTermProfileMemory
from app.memory.episodic import EpisodicMemory
from app.memory.semantic import SemanticMemory
from app.memory.extractor import extract_profile_update
from app.utils.key_manager import GeminiKeyManager


load_dotenv()

short_term = ConversationBufferMemory()
long_term = LongTermProfileMemory()
episodic = EpisodicMemory()
semantic = SemanticMemory()

key_manager = GeminiKeyManager()
client = genai.Client(api_key=key_manager.get_current_key())


def save_memory(state: MemoryState):
    query = state["query"]
    user_id = state["user_id"]

    profile_updates = extract_profile_update(query)

    if profile_updates:
        long_term.update_profile(user_id, profile_updates)

    if any(word in query.lower() for word in ["lỗi", "fix", "sửa", "hoàn tất", "xong"]):
        episodic.add_event(
            user_id=user_id,
            event=query,
            solution="Saved as user experience."
        )

    short_term.add("user", query)

    return state


def retrieve_memory(state: MemoryState):
    user_id = state["user_id"]
    query = state["query"]

    state["user_profile"] = long_term.get_profile(user_id)
    state["episodes"] = episodic.search_events(user_id, query)
    state["semantic_hits"] = semantic.search(query)
    state["recent_conversation"] = short_term.get()
    state["memory_budget"] = 2500

    used = ["short_term"]

    if state["user_profile"]:
        used.append("long_term_profile")

    if state["episodes"]:
        used.append("episodic")

    if state["semantic_hits"]:
        used.append("semantic")

    state["memory_used"] = "+".join(used)

    return state


def build_prompt_node(state: MemoryState):
    state["prompt"] = build_prompt(state)
    return state


def fallback_answer(state: MemoryState):
    query = state["query"].lower()
    profile = state["user_profile"]
    semantic_hits = state["semantic_hits"]
    episodes = state["episodes"]

    if "backend" in query:
        return profile.get("backend_preference", "Tôi chưa biết bạn thích backend nào.")

    if "dị ứng" in query:
        return profile.get("allergy", "Tôi chưa biết bạn dị ứng gì.")

    if "đã từng" in query or "trước đây" in query:
        if episodes:
            return f"Có, trước đây bạn đã gặp: {episodes[-1]['event']}"
        return "Tôi chưa thấy episodic memory liên quan."

    if "là gì" in query or "rule" in query:
        if semantic_hits:
            return semantic_hits[0]["content"]
        return "Tôi chưa có semantic memory phù hợp."

    return "Tôi đã ghi nhận thông tin của bạn."


def answer_node(state: MemoryState):
    global client

    prompt = state["prompt"]

    try:
        result = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        answer = result.text.strip()

    except Exception as e:
        error_text = str(e)

        if "429" in error_text or "quota" in error_text.lower() or "RESOURCE_EXHAUSTED" in error_text:
            try:
                new_key = key_manager.rotate_key()
                print("Switching Gemini API key...")
                client = genai.Client(api_key=new_key)

                result = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                answer = result.text.strip()

            except Exception:
                answer = fallback_answer(state)
        else:
            answer = fallback_answer(state)

    state["response"] = answer

    # Chỉ lưu final answer, không lưu full prompt
    short_term.add("assistant", answer)

    return state


def build_graph():
    workflow = StateGraph(MemoryState)

    workflow.add_node("save_memory", save_memory)
    workflow.add_node("retrieve_memory", retrieve_memory)
    workflow.add_node("build_prompt", build_prompt_node)
    workflow.add_node("answer", answer_node)

    workflow.set_entry_point("save_memory")
    workflow.add_edge("save_memory", "retrieve_memory")
    workflow.add_edge("retrieve_memory", "build_prompt")
    workflow.add_edge("build_prompt", "answer")
    workflow.add_edge("answer", END)

    return workflow.compile()