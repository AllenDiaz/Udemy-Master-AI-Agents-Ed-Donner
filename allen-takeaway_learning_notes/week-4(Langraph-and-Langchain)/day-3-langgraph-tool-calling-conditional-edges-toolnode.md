# LangGraph — Tool Calling with Conditional Edges and ToolNode

## Overview

This lesson adds tool calling to the LangGraph chatbot using LangChain's `bind_tools()`, LangGraph's built-in `ToolNode`, and a `conditional_edge` — demonstrating how tool calling integrates naturally into the graph structure.

---

## Two Places Where Tools Are Handled

| Place | Responsibility |
|---|---|
| **LLM node** (`chatbot`) | Passes tool definitions to the model (the JSON schema) |
| **Tools node** (`tools`) | Receives tool call requests from the model and executes them |

This mirrors Week 1's manual approach (`handle_tool_calls`) — LangGraph just makes it cleaner.

---

## State — TypedDict (Alternative to Pydantic)

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
```

> Both `TypedDict` and Pydantic `BaseModel` are valid — behavior is identical. Use whichever you prefer.

---

## LLM with Tools — `bind_tools()`

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)   # auto-generates tool JSON on every call
```

`bind_tools()` creates a version of the LLM that automatically:
- Builds the tool JSON schema on every invocation
- Parses tool call requests from responses

---

## The Chatbot Node

```python
def chatbot_node(old_state: State) -> State:
    response = llm_with_tools.invoke(old_state["messages"])
    return {"messages": [response]}

graph_builder.add_node("chatbot", chatbot_node)
```

---

## The Tools Node (Built-in)

```python
from langgraph.prebuilt import ToolNode

tool_node = ToolNode(tools=tools)   # handles tool execution automatically
graph_builder.add_node("tools", tool_node)
```

`ToolNode` is a pre-built node that:
- Detects tool call requests in the latest message
- Finds and executes the matching tool function
- Returns the tool result as a message

---

## Edges — Conditional Routing

```python
from langgraph.prebuilt import tools_condition

# START → chatbot (always)
graph_builder.add_edge(START, "chatbot")

# chatbot → tools (only if model wants to call a tool)
graph_builder.add_conditional_edges("chatbot", tools_condition)

# tools → chatbot (always — feed result back for continued processing)
graph_builder.add_edge("tools", "chatbot")
```

### `tools_condition` — The Built-in If Statement

`tools_condition` checks whether the model's response has `finish_reason == "tool_calls"`:
- **True** → route to `tools` node
- **False** → route to `END`

> This is the same `if finish_reason == "tool_calls"` check from Week 1 — now handled declaratively as a graph edge.

---

## Compiled Graph Structure

```
START
  │
  ▼
[chatbot] ──── tools_condition ──── (tool call?) ──── [tools]
  ▲                                                       │
  └───────────────────────────────────────────────────────┘
  │
  ▼ (no tool call)
 END
```

- Solid line = always taken
- Dotted/conditional line = only if tool call requested
- `tools → chatbot` loop feeds results back for continued reasoning

---

## Running the Graph

```python
def chat(user_input: str, history):
    initial_state = {"messages": [{"role": "user", "content": user_input}]}
    result = graph.invoke(initial_state)
    return result["messages"][-1].content

gr.ChatInterface(chat, type="messages").launch()
```

**Live demo result:**

> *"Please send me a push notification with the current USD to GBP exchange rate."*
>
> 1. Agent searched: `current USD to GBP exchange rate` → 0.78
> 2. Agent called `send_push_notification("The current USD/GBP rate is 0.78")`
> 3. Push notification received ✅

Two tool calls, one prompt, fully autonomous.

---

## Verifying in LangSmith

After running, the LangSmith trace shows:
- Full message chain
- `search` tool call with query and result
- `send_push_notification` tool call
- Token usage and latency per step

---

## Key Takeaways

- `bind_tools()` handles all tool JSON schema generation — no manual JSON needed
- `ToolNode` handles all tool execution — no manual `handle_tool_calls()` needed
- `tools_condition` is the built-in conditional edge for tool routing
- The `tools → chatbot` back edge is essential — without it, tool results are never processed
- `tools_condition` automatically adds an `END` path for when no tool call is made
- LangSmith makes the full execution trace visible — invaluable for debugging multi-tool flows

---

## Up Next

Adding **checkpointing** to preserve conversation history across super steps (multiple invocations).