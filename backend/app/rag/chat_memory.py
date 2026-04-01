"""
CHAT MEMORY MODULE
==================
Per-user, in-memory conversation history for context-aware RAG chat.

Design:
  - Stores the last MAX_HISTORY turns (user + assistant alternating) per user.
  - Injected as a "PREVIOUS CONVERSATION" block in every Gemini prompt.
  - Enables natural follow-ups: "explain more", "compare with previous answer".
  - Pure in-process dict — no external dependencies, no DB round-trips.
  - Memory is lost on server restart (acceptable for a demo / MVP; swap for
    Redis or SQLite persistence if you need durability across restarts).
"""

from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, List

# ── Configuration ─────────────────────────────────────────────────────────────
MAX_HISTORY = 10   # Maximum conversation turns (user + assistant) kept per user


# ── Internal store ────────────────────────────────────────────────────────────
# { user_id: [ { "role": "user"|"assistant", "content": str, "ts": ISO-str } ] }
_store: Dict[int, List[Dict]] = defaultdict(list)


# ── Public API ────────────────────────────────────────────────────────────────

def add_turn(user_id: int, role: str, content: str) -> None:
    """
    Append one conversational turn to the user's history.

    Args:
        user_id:  Authenticated user's DB id.
        role:     "user" or "assistant".
        content:  The message text.
    """
    _store[user_id].append({
        "role":    role,
        "content": content,
        "ts":      datetime.now(timezone.utc).isoformat(),
    })
    # Trim to the most recent MAX_HISTORY entries
    if len(_store[user_id]) > MAX_HISTORY:
        _store[user_id] = _store[user_id][-MAX_HISTORY:]


def get_history(user_id: int) -> List[Dict]:
    """Return a copy of the user's full conversation history."""
    return list(_store[user_id])


def clear_history(user_id: int) -> None:
    """Wipe the user's conversation history (e.g. on explicit reset)."""
    _store[user_id] = []


def build_context_block(user_id: int) -> str:
    """
    Format prior turns into a plain-text block suitable for Gemini prompts.

    Returns an empty string when there is no history yet, so callers can
    safely include it in prompts without extra logic.

    Example output:
        === CONVERSATION HISTORY ===
        User: What methods are used in the study?
        Assistant: The study uses a mixed-methods approach ...
        User: Explain more about the quantitative part.
        === END OF HISTORY ===
    """
    history = get_history(user_id)
    if not history:
        return ""

    lines = ["=== CONVERSATION HISTORY ==="]
    for turn in history:
        label = "User" if turn["role"] == "user" else "Assistant"
        lines.append(f"{label}: {turn['content']}")
    lines.append("=== END OF HISTORY ===")
    return "\n".join(lines)
