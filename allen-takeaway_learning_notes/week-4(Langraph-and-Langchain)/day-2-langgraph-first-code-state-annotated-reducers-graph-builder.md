# LangGraph — First Code (State, Annotated, Reducers & Graph Builder)

## Overview

This lesson moves from theory to code — implementing the first two steps of building a LangGraph: defining the state class with a reducer using `Annotated`, and starting the graph builder.

---

## Python Type Hints (Quick Recap)

```python
def shout(text: str) -> str:
    return text.upper()
```

Type hints (`str`, `int`, `list`, etc.) are optional annotations — they don't change behavior but improve readability and tooling.

---

## `Annotated` — Adding Extra Information to Types

`Annotated` lets you attach extra metadata to a type hint. Python ignores it, but other tools (like LangGraph) can read it.

```python
from typing import Annotated

# Python ignores "something to be shouted" — but LangGraph can use annotations
def shout(text: Annotated[str, "something to be shouted"]) -> str:
    return text.upper()
```

> **Key insight:** LangGraph uses `Annotated` to let you specify a **reducer function** for a state field.

---

## Step 1 — Define the State Class

State can be defined as a Pydantic `BaseModel` or a `TypedDict`. This lesson uses Pydantic.

```python
from typing import Annotated
from pydantic import BaseModel
from langgraph.graph.message import add_messages

class State(BaseModel):
    messages: Annotated[list, add_messages]
```

**Breaking this down:**

| Part | Meaning |
|---|---|
| `messages` | Field name — stores the conversation history |
| `list` | The type — a list of messages |
| `add_messages` | The **reducer** — tells LangGraph how to combine updates to this field |

### What `add_messages` Does
A built-in LangGraph reducer that **concatenates** lists instead of overwriting:
- Old state: `messages = [msg1, msg2]`
- Node returns: `messages = [msg3]`
- Result after reducer: `messages = [msg1, msg2, msg3]` ✅

Without reducer: `messages = [msg3]` ❌ (overwrites)

---

## Step 2 — Start the Graph Builder

```python
from langgraph.graph import StateGraph

graph_builder = StateGraph(State)   # pass the CLASS, not an instance
```

> Note: You pass in `State` (the class/type), not `State()` (an instance). The graph builder uses it as a schema to understand the structure of state throughout the graph.

---

## Five Steps — Progress So Far

| Step | Action | Status |
|---|---|---|
| 1 | Define state class | ✅ Done |
| 2 | Start graph builder | ✅ Done |
| 3 | Create nodes | ⏳ Next |
| 4 | Create edges | ⏳ Next |
| 5 | Compile the graph | ⏳ Next |

---

## Key Takeaways

- `Annotated[list, add_messages]` is the pattern for attaching a reducer to a state field
- `add_messages` is LangGraph's built-in reducer for message lists — appends, doesn't overwrite
- Pass the **class** to `StateGraph`, not an instance
- State is always a Pydantic model or TypedDict — both are valid
- Without a reducer on `messages`, parallel nodes would overwrite each other's messages

---

## Imports Reference

```python
from typing import Annotated
from pydantic import BaseModel
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv(override=True)
```

---

## Up Next

Steps 3–5: Creating nodes (LLM calls as functions), adding edges, compiling the graph, and invoking it.