# LangGraph — Real LLM Chatbot Node with ChatOpenAI

## Overview

This lesson replaces the silly random node with a real LLM call using **ChatOpenAI** from LangChain, completing a working LangGraph chatbot — and exposes a key limitation: no conversation history across invocations.

---

## Why LangChain's ChatOpenAI?

LangGraph doesn't require LangChain, but:
- Most community examples use LangChain LLMs with LangGraph
- `ChatOpenAI` integrates seamlessly — `.invoke()` accepts the messages list directly
- You can substitute any LLM (direct API call, OpenAI SDK, etc.)

---

## Full Graph — All 5 Steps

```python
from typing import Annotated
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

# Step 1 — State
class State(BaseModel):
    messages: Annotated[list, add_messages]

# Step 2 — Graph builder
graph_builder = StateGraph(State)

# Step 3 — Node (real LLM call)
llm = ChatOpenAI(model="gpt-4o-mini")

def chatbot_node(old_state: State) -> State:
    response = llm.invoke(old_state.messages)   # LangChain invoke
    return State(messages=[response])           # response is an AIMessage object

graph_builder.add_node("chatbot", chatbot_node)

# Step 4 — Edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Step 5 — Compile
graph = graph_builder.compile()
```

**Graph structure:**
```
START → chatbot → END
```

---

## Running the Graph with Gradio

```python
import gradio as gr

def chat(user_input: str, history):
    initial_state = State(messages=[{"role": "user", "content": user_input}])
    result = graph.invoke(initial_state)
    return result["messages"][-1].content

gr.ChatInterface(chat, type="messages").launch()
```

---

## The Limitation: No Conversation History

Each `graph.invoke()` call starts fresh — only the current message is in state:

```
User: "My name's Ed."
Bot:  "Nice to meet you, Ed!"

User: "What's my name?"
Bot:  "I'm sorry, I don't have access to your personal data."  ← no memory
```

**Why?** Every invocation creates a new `State` with only the latest user message. Prior messages are never passed in — the graph has no memory across calls.

---

## What's Happening in `result["messages"]`

The `add_messages` reducer packages everything into typed objects:

```python
result["messages"] = [
    HumanMessage(content="My name's Ed."),
    AIMessage(content="Nice to meet you, Ed!")
]
```

- `HumanMessage` — the user's input
- `AIMessage` — the LLM's response (returned directly by `llm.invoke()`)

---

## Key Takeaways

- `llm.invoke(messages)` takes the messages list and returns an `AIMessage` — plug it straight into the new state
- The node pattern is always: receive state → do work → return new state
- LangGraph itself has no built-in memory across separate `invoke()` calls — this must be added explicitly
- `result["messages"][-1].content` is the standard way to extract the latest response

---

## Up Next

Adding **conversation history** (memory across invocations) and **tools** to the LangGraph chatbot.