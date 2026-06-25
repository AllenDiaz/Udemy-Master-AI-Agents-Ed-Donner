# LangGraph — State Immutability and Reducers

## Overview

This lesson goes deeper on two critical LangGraph concepts before the first coding session: **state immutability** and **reducers** — the mechanism that allows multiple nodes to safely update state in parallel.

---

## State Immutability

**Immutable** = once created, the object's contents are never changed (mutated).

In LangGraph, state represents a **snapshot** — you never modify it in place. Instead, every node:
1. Receives the current state as input
2. Does its work
3. Returns a **new state object** with the updated values

### Example: Counting Node

```python
def my_counting_node(old_state: MyState) -> MyState:
    new_count = old_state.count + 1
    return MyState(count=new_count)   # new object — never mutate old_state
```

> ❌ Don't do: `old_state.count += 1`  
> ✅ Do: return a new `MyState(count=old_state.count + 1)`

**Why immutability matters:**
- Preserves the snapshot — you can always go back to any prior state
- Enables checkpointing and "time travel"
- Makes parallel execution safe

---

## Reducers

A **reducer** is an optional function you can attach to a specific field in your state class.

### What It Does

When a node returns a new state, LangGraph uses the reducer to **combine** the new field value with the existing state value — rather than simply overwriting it.

### Why You Need It

When **multiple nodes run in parallel**, they each return their own updated state. Without a reducer, one node's update could silently overwrite another's.

With a reducer, LangGraph knows *how* to merge concurrent updates for that field safely.

### The Most Common Reducer: `add`

Used for list fields — instead of replacing the list, it **appends** new items to it.

```python
from typing import Annotated
from langgraph.graph import add_messages

class MyState(TypedDict):
    messages: Annotated[list, add_messages]   # reducer = add_messages
    count: int                                 # no reducer — simple overwrite
```

> `Annotated[list, add_messages]` tells LangGraph: "when updating `messages`, append — don't replace."

---

## State Field Behavior Summary

| Field type | Reducer? | Behavior on update |
|---|---|---|
| Simple value (int, str) | No | Overwrites with new value |
| List with reducer | Yes (`add_messages`) | Appends new items to existing list |
| Custom field | Optional | Whatever your reducer function defines |

---

## Mental Model

```
Node A runs → returns new_state_A
Node B runs → returns new_state_B  (parallel)
                    │
                    ▼
         LangGraph applies reducer
                    │
                    ▼
         Combined state passed to next node
```

Without reducer → B might overwrite A's changes  
With reducer → both updates are merged correctly

---

## Key Takeaways

- State is **immutable** — always return a new state object, never mutate the input
- A **reducer** is a function attached to a state field that defines how to merge concurrent updates
- Reducers are what make **parallel node execution** safe
- The most common reducer is `add_messages` — appends to a messages list
- If a field has no reducer, the new value simply overwrites the old one
- This will become concrete in the next lesson when we write actual LangGraph code

---

## Up Next

Writing the first LangGraph graph — state class with reducers, nodes, edges, compilation, and invocation.