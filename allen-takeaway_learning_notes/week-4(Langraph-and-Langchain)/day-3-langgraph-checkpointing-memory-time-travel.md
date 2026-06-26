# LangGraph — Checkpointing, Memory & Time Travel

## Overview

This lesson adds **checkpointing** to the LangGraph chatbot — enabling true conversation memory across super steps (separate `graph.invoke()` calls) — and demonstrates **time travel**: the ability to restore any prior state snapshot.

---

## The Problem (Recap)

Even with reducers and state management, each `graph.invoke()` starts fresh:
- State is managed **within** a super step ✅
- State is **not** preserved **between** super steps ❌

```
User: "My name is Ed."   → invoke() → "Nice to meet you, Ed!"
User: "What's my name?"  → invoke() → "I don't have access to your personal info." ❌
```

---

## The Solution: Checkpointing

A **checkpointer** saves a snapshot of the state after each super step. On the next invocation, it reloads that snapshot — giving the agent full conversation history.

### `MemorySaver` — In-Memory Checkpointer

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()   # stores checkpoints in RAM (not disk)
```

> Note: "MemorySaver" = saves to in-memory storage (RAM), not "saves memories" — slightly confusing naming.

### Adding to the Graph — One Line Change

```python
graph = graph_builder.compile(checkpointer=memory)   # ← only change
```

That's it. The graph looks identical — checkpointing is transparent.

---

## Thread ID — Conversation Grouping

Every invocation must include a `config` with a `thread_id` to identify which conversation slot to use:

```python
config = {"configurable": {"thread_id": "1"}}

result = graph.invoke(initial_state, config=config)
```

- `thread_id` = a conversation thread identifier (not an OS thread)
- Same `thread_id` → same memory slot → agent remembers prior turns
- Different `thread_id` → separate memory slot → fresh conversation

---

## Full Chat Function with Checkpointing

```python
config = {"configurable": {"thread_id": "1"}}

def chat(user_input: str, history):
    initial_state = {"messages": [{"role": "user", "content": user_input}]}
    result = graph.invoke(initial_state, config=config)
    return result["messages"][-1].content

gr.ChatInterface(chat, type="messages").launch()
```

**Demo:**
```
User: "My name is Ed."   → "Nice to meet you, Ed!"
User: "What's my name?"  → "Your name is Ed." ✅
```

The memory persists even after relaunching the Gradio UI — it's stored in `memory`, not in the UI.

---

## Inspecting State

### Get Current State

```python
state_snapshot = graph.get_state(config)
# Returns full conversation history, current messages, metadata
```

### Get Full State History

```python
history = list(graph.get_state_history(config))
# Returns every super step snapshot, most recent first
```

---

## Time Travel — Rewinding State

Every checkpoint has a unique `checkpoint_id`. You can rewind to any prior moment by passing it in config:

```python
# Rewind to a specific checkpoint
past_config = {
    "configurable": {
        "thread_id": "1",
        "checkpoint_id": "some-past-checkpoint-id"
    }
}

result = graph.invoke(None, config=past_config)   # replay from that point
```

**Use cases:**
- Restart a failed agent run from the last good checkpoint
- Replay a workflow to debug unexpected behavior
- Build repeatable, auditable agent systems

---

## Thread Isolation Demo

```python
# Thread 1 — knows your name
config_1 = {"configurable": {"thread_id": "1"}}

# Thread 2 — separate memory, knows nothing
config_2 = {"configurable": {"thread_id": "2"}}

# Reset all memory
memory = MemorySaver()   # create new instance → all threads wiped
graph = graph_builder.compile(checkpointer=memory)
```

---

## Checkpointing vs. Reducer — Summary

| | Reducer (`add_messages`) | Checkpointer (`MemorySaver`) |
|---|---|---|
| **Scope** | Within a single super step | Between separate super steps |
| **Purpose** | Merge parallel node updates safely | Persist conversation across invocations |
| **Storage** | In-flight state object | RAM (or DB for persistent storage) |

---

## Key Takeaways

- `checkpointer=memory` in `compile()` is the only code change needed to enable memory
- `thread_id` in config groups invocations into a conversation thread
- Checkpointing persists in the `MemorySaver` object — independent of the UI
- `get_state()` and `get_state_history()` expose full conversation snapshots
- Time travel = rewinding to any checkpoint by `checkpoint_id` — enables robust, repeatable agents
- For production: swap `MemorySaver` for a SQLite or PostgreSQL checkpointer to persist across restarts

---

## Up Next

Building the full LangGraph project — a practical application with tools, memory, and a polished UI.