# LangGraph — Persistent Memory with SQLite Checkpointer

## Overview

This lesson upgrades the in-memory checkpointer to a **SQLite-based checkpointer** — enabling conversation memory that persists across kernel restarts and application shutdowns. A one-word change in the code.

---

## Switching from MemorySaver to SQLiteSaver

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Create SQLite checkpointer — writes to a .db file
memory = SqliteSaver.from_conn_string("memory.db")

# Compile graph — same as before
graph = graph_builder.compile(checkpointer=memory)
```

**That's the only change.** Everything else — thread IDs, config, `graph.invoke()` — stays identical.

---

## MemorySaver vs. SqliteSaver

| | `MemorySaver` | `SqliteSaver` |
|---|---|---|
| **Storage** | RAM | SQLite `.db` file on disk |
| **Persistence** | Lost on kernel restart | Survives restarts ✅ |
| **Setup** | None | File path string |
| **Use case** | Development / testing | Production / long-running agents |

---

## Proof of Persistence

After switching to `SqliteSaver`:

1. Told the agent: *"My name is Ed."*
2. **Restarted the Jupyter kernel** — all variables wiped
3. Rebuilt graph with same `SqliteSaver` pointing to `memory.db`
4. Asked: *"Hello"* → Agent responded: *"Hello again, Ed!"* ✅

Memory survived a full kernel restart — stored in the SQLite database file.

---

## Memory + Tools Together

With SQLite checkpointing and tools active simultaneously:

```
Turn 1: "Please send me a push notification with the current USD/GBP rate."
→ Agent searches web → finds 0.78 → sends push notification ✅

Turn 2: "Can you send that push notification again please?"
→ Agent recalls rate from memory (no new search) → sends push notification ✅
```

LangSmith trace confirmed:
- Turn 2 did **not** call the search tool — used cached value from memory
- Only `send_push_notification` was called
- Full conversation history visible in context

---

## Full Checkpointing Picture

```
[Define Graph] ← once at startup

User turn 1 → [invoke] → response → checkpoint saved ──────► memory.db
User turn 2 → [invoke] → loads checkpoint → response → checkpoint saved ─► memory.db
User turn 3 → [invoke] → loads checkpoint → response → checkpoint saved ─► memory.db
```

- Each super step is checkpointed
- Thread ID keys the memory slot
- Any checkpoint can be restored (time travel)
- SQLite makes it durable across restarts

---

## Key Takeaways

- Switching checkpointers is a **one-line change** — `MemorySaver` → `SqliteSaver`
- SQLite checkpointing gives true persistence with zero infrastructure overhead
- Memory + tools work together naturally — agent uses memory to avoid redundant tool calls
- For production at scale: swap `SqliteSaver` for PostgreSQL checkpointer
- The thread ID is the key that connects all super steps into one conversation thread

---

## Day 3 Recap — What Was Covered

| Topic | Key Concept |
|---|---|
| LangSmith | Observability — traces, costs, token usage |
| Tools with `bind_tools()` | Auto-generates tool JSON for LLM |
| `ToolNode` | Built-in node for executing tool calls |
| `tools_condition` | Conditional edge routing for tool calls |
| `MemorySaver` | In-memory checkpointing |
| `SqliteSaver` | Persistent checkpointing to disk |
| Time travel | Rewinding to any prior checkpoint by ID |

---

## Up Next

**The Sidekick Project** — a full LangGraph application with tools, persistent memory, and a polished UI, designed with real business value.