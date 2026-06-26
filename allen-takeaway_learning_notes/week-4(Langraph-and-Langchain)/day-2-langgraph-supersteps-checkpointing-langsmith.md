# LangGraph — Super Steps, Checkpointing & LangSmith

## Overview

This lesson introduces three key LangGraph concepts that enable production-ready agent workflows: **LangSmith** for observability, **tools** (built-in and custom), and — most importantly — **super steps** and **checkpointing** for memory across conversations.

---

## What Is a Super Step?

> A super step = **one complete invocation of the graph** from START to END.

| Concept | Description |
|---|---|
| **Super step** | One full `graph.invoke()` call — all nodes run to completion |
| **Parallel nodes** | Nodes running at the same time = part of the **same** super step |
| **Sequential nodes** | Nodes running one after another = **separate** super steps |

### Common Misconception

❌ You might think: a graph represents the back-and-forth between user and agent  
✅ Reality: **each user message = a new `graph.invoke()` call = a new super step**

```
User: "What's the weather?"     → invoke() → super step 1
User: "What about tomorrow?"    → invoke() → super step 2
User: "And next week?"          → invoke() → super step 3
```

Each invocation runs the **entire graph from scratch**.

---

## Super Steps Visualized

```
[Define Graph] ← done once at startup

User message 1 → [invoke graph] → response    ← super step 1
                      │
User message 2 → [invoke graph] → response    ← super step 2
                      │
User message 3 → [invoke graph] → response    ← super step 3
```

> The reducer manages state **within** a super step (across parallel nodes).  
> The reducer does **not** carry state **between** super steps — that's what checkpointing is for.

---

## Why This Matters for Memory

Without checkpointing, each `graph.invoke()` starts with a blank state — no memory of prior conversations (as demonstrated in the previous lesson where the bot forgot the user's name).

To preserve context **across super steps**, LangGraph provides **checkpointing**.

---

## Checkpointing

A checkpoint is a **frozen snapshot of the state** saved after each super step.

When the next super step begins, LangGraph can **reload the last checkpoint** and continue from where it left off — giving the agent full conversation history.

```
Super step 1 → runs → state saved as checkpoint ✓
Super step 2 → loads checkpoint → runs with full history → saves new checkpoint ✓
Super step 3 → loads checkpoint → runs with full history → saves new checkpoint ✓
```

This is what enables true **multi-turn conversation memory** in LangGraph.

---

## LangSmith — Observability

LangSmith is LangChain's monitoring tool — connects with LangGraph to provide:
- Visibility into every node execution
- Full trace of messages sent and received
- Debugging failed runs
- Token usage per call

Set up by adding to `.env`:
```bash
LANGCHAIN_API_KEY=your_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=your_project_name
```

Once set, all `graph.invoke()` calls are automatically logged to LangSmith.

---

## What's Coming in the Lab

| Topic | Description |
|---|---|
| **LangSmith** | See graph invocations logged in real time |
| **Built-in tools** | Use LangGraph's out-of-the-box tools (e.g. web search) |
| **Custom tools** | Build and attach a custom tool to the graph |
| **Checkpointing** | Add memory across super steps using a checkpointer |

---

## Key Takeaways

- A **super step** = one full `graph.invoke()` — not one node, not one message exchange
- The **reducer** handles state merging **within** a super step (parallel nodes)
- The **checkpointer** handles state persistence **between** super steps (across conversations)
- Without checkpointing, every invocation is stateless — the bot forgets everything
- LangSmith provides the observability layer — essential for debugging complex graphs

---

## Related Concepts

- `add_messages` reducer — merges messages within a super step
- `MemorySaver` / SQLite checkpointer — common checkpointer implementations
- LangSmith tracing — `LANGCHAIN_TRACING_V2=true`
- Human-in-the-loop — pausing and resuming a graph mid-super-step