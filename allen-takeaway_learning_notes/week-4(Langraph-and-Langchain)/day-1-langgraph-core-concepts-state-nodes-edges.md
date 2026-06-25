# LangGraph Core Concepts — State, Nodes, Edges & Graph Building

## Overview

This lesson introduces LangGraph's core terminology and the two-phase execution model used to build and run agent workflows as graphs.

---

## Core Terminology

### Graph
The top-level structure representing an entire agent workflow — a tree-like structure of connected operations.

### State
- A **snapshot of the current status** of the entire application
- Shared across the whole graph — every node sees it
- Treat as **immutable** — nodes receive a state and return a *new* state (a diff), not a mutated one
- Defined as a Python class

### Nodes
- The **points on the graph** — each node is a **Python function**
- Represent a piece of logic or operation (e.g. call an LLM, write a file, process data)
- Receive the current **state** as input
- Return an **updated state** as output

```
Node = Python function
    Input:  current state
    Output: updated state (delta)
```

### Edges
- The **connections between nodes** — also Python functions
- Determine **which node runs next** based on the current state
- Two types:

| Type | Behavior |
|---|---|
| **Simple edge** | Always goes to the next node unconditionally |
| **Conditional edge** | Chooses the next node based on a condition in the state |

---

## Nodes vs. Edges — One-Liner Summary

> **Nodes do the work. Edges decide what's next.**

---

## Visual Model

```
        ┌─────────┐
        │  Node A │  (does something, updates state)
        └────┬────┘
             │ simple edge
        ┌────▼────┐
        │  Node B │  (does something, updates state)
        └────┬────┘
             │ conditional edge
      ┌──────┴──────┐
      ▼             ▼
 [Node C]       [Node D]
(condition met) (condition not met)
```

---

## The Two-Phase Execution Model

Running a LangGraph application involves **two distinct phases**:

### Phase 1 — Define the Graph (at startup)
Build the graph structure before anything runs:

1. **Define the state class** — the schema for your application's state
2. **Start the graph builder** — `StateGraph(StateClass)`
3. **Create nodes** — add Python functions as nodes
4. **Create edges** — connect nodes with simple or conditional edges
5. **Compile the graph** — turns the definition into an executable object

### Phase 2 — Run the Graph
Invoke the compiled graph with an initial state — it executes node by node following the edges.

```python
# Phase 1 — Define
graph_builder = StateGraph(MyState)
graph_builder.add_node("node_a", my_function)
graph_builder.add_edge("node_a", "node_b")
graph = graph_builder.compile()

# Phase 2 — Run
graph.invoke(initial_state)
```

> This two-phase pattern is unusual compared to normal Python code — you first *describe* what you want to happen, then *execute* it. Think of Phase 1 as writing a program, Phase 2 as running it.

---

## Five Steps to Build Your First Graph

| Step | Action |
|---|---|
| 1 | Define your **state class** |
| 2 | Start the **graph builder** |
| 3 | Create **nodes** (Python functions) |
| 4 | Create **edges** (connections between nodes) |
| 5 | **Compile** the graph, then **invoke** it |

> Note: There is an important concept called the **reducer** associated with the state class — covered in the next lesson when we write actual code.

---

## Key Takeaways

- **Graph** = the full workflow; **State** = shared data; **Nodes** = functions that do work; **Edges** = functions that decide what's next
- State is immutable — always return a new state, never mutate the existing one
- The two-phase model (define then run) is the core mental shift when coming from CrewAI or OpenAI Agents SDK
- Conditional edges are how LangGraph handles branching and decision-making
- The graph builder lays out the *structure* before anything actually executes

---

## Up Next

Writing the actual LangGraph code — state class, nodes, edges, compilation, and running the first graph.