# LangGraph — Building and Running the First Graph

## Overview

This lesson completes all five steps of building a LangGraph — creating a node, adding edges, compiling, and invoking the graph — using a deliberately silly "random noun + adjective" node to prove that LangGraph has nothing to do with LLMs specifically.

---

## Step 3 — Create a Node

A node is a Python function that takes the current state and returns a new state.

```python
import random

nouns = ["muffins", "penguins", "pickles"]
adjectives = ["haunted", "sparkly", "outrageous", "untrustworthy"]

def our_first_node(old_state: State) -> State:
    reply = f"{random.choice(nouns)} are {random.choice(adjectives)}"
    new_state = State(messages=[{"role": "assistant", "content": reply}])
    return new_state

# Register the node with the graph builder
graph_builder.add_node("first_node", our_first_node)
```

**Key points:**
- `old_state` is received but not mutated
- A brand new `State` instance is created and returned
- The node is registered with `add_node(name, function)`

---

## Step 4 — Create Edges

```python
from langgraph.graph import START, END

graph_builder.add_edge(START, "first_node")   # entry point → node
graph_builder.add_edge("first_node", END)     # node → exit
```

- `START` and `END` are built-in LangGraph constants
- Every graph needs a path from `START` to `END`

---

## Step 5 — Compile the Graph

```python
graph = graph_builder.compile()
```

Optionally visualize the compiled graph:
```python
graph.get_graph().draw_mermaid_png()
```

Result:
```
START → first_node → END
```

---

## Running the Graph — `invoke()`

```python
def chat(user_message: str, history: list):
    input_state = State(messages=[{"role": "user", "content": user_message}])
    result = graph.invoke(input_state)
    return result["messages"][-1].content
```

- `graph.invoke(state)` executes the full graph with the given initial state
- Returns the final state after all nodes have run
- `invoke` is the standard LangGraph (and LangChain) execution method

---

## What Comes Back from `invoke()`

The result contains `messages` as a list of typed message objects:

```python
# result["messages"] looks like:
[
    HumanMessage(content="hi there"),
    AIMessage(content="muffins are haunted")
]
```

This is the `add_messages` reducer at work — it:
1. Concatenates the new messages onto the existing list
2. Automatically packages raw dicts into `HumanMessage` / `AIMessage` objects

---

## Complete First Graph — All 5 Steps

```python
from typing import Annotated
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Step 1 — State
class State(BaseModel):
    messages: Annotated[list, add_messages]

# Step 2 — Graph builder
graph_builder = StateGraph(State)

# Step 3 — Node
def our_first_node(old_state: State) -> State:
    reply = f"{random.choice(nouns)} are {random.choice(adjectives)}"
    return State(messages=[{"role": "assistant", "content": reply}])

graph_builder.add_node("first_node", our_first_node)

# Step 4 — Edges
graph_builder.add_edge(START, "first_node")
graph_builder.add_edge("first_node", END)

# Step 5 — Compile
graph = graph_builder.compile()

# Run
result = graph.invoke(State(messages=[{"role": "user", "content": "hi"}]))
```

---

## Key Takeaways

- Nodes are **just Python functions** — no LLM required
- `graph.invoke(state)` is how you execute a compiled graph
- `START` and `END` are built-in constants for graph entry/exit points
- `add_messages` reducer packages raw dicts into typed `HumanMessage`/`AIMessage` objects automatically
- The graph setup (steps 1–5) is completely decoupled from what the nodes actually do
- Any Python logic can be a node — the power comes from connecting them in a graph

---

## Up Next

Replacing the silly random node with a real LLM call — building the first proper LangGraph agent.