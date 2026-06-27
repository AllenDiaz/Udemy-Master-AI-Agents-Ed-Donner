# LangGraph — Playwright Browser Agent (Lab 3)

## Overview

This lesson wires the Playwright browser toolkit into a full LangGraph agent — giving it the ability to autonomously navigate websites, extract content, and send push notifications. The agent drives a real browser window with no human interaction.

---

## Combining Tools

```python
# Dictionary comprehension to look up specific tools by name
tools_by_name = {tool.name: tool for tool in playwright_tools}

navigate_tool = tools_by_name["navigate_browser"]
extract_text_tool = tools_by_name["extract_text"]

# Test tools directly (no LLM needed)
await navigate_tool.arun({"url": "https://www.cnn.com"})
text = await extract_text_tool.arun({})
```

Then combine all tools into one list:

```python
tools = playwright_tools + [tool_push]   # browser tools + push notification
```

---

## LLM + Chatbot Node

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)   # binds ALL tools (browser + push)

def chatbot_node(old_state: State) -> State:
    response = llm_with_tools.invoke(old_state["messages"])
    return {"messages": [response]}
```

---

## Graph — Same Pattern, Meatier Tools

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot_node)
graph_builder.add_node("tools", ToolNode(tools=tools))

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
```

**Graph structure:** identical to Lab 2 — the power comes from the tools, not the graph shape.

---

## Async Gradio Chat Function

```python
import gradio as gr

config = {"configurable": {"thread_id": "1"}}

async def chat(user_input: str, history):
    initial_state = {"messages": [{"role": "user", "content": user_input}]}
    result = await graph.ainvoke(initial_state, config=config)
    return result["messages"][-1].content

gr.ChatInterface(chat, type="messages").launch()
```

> History from Gradio is ignored — checkpointing handles memory instead.

---

## Live Demo Results

### Request 1: News headline push notification
> *"Please send me a push notification with a news headline from CNN."*

Agent steps (visible in LangSmith):
1. `navigate_browser` → `https://www.cnn.com`
2. `extract_hyperlinks` → scanned headlines
3. `extract_text` → read content
4. `send_push_notification` → delivered headline ✅

### Request 2: USD/GBP exchange rate
> *"Please send me a push notification with the current USD/GBP exchange rate."*

Agent steps:
1. `navigate_browser` → exchange rates page
2. `extract_text` → found rate (0.77)
3. `send_push_notification` → delivered rate ✅

---

## LangSmith Trace Insights

- Full tool call chain visible: navigate → extract → push
- Total cost for entire conversation: **~0.8 cents**
- Token count visible per call
- Tool returning `null` noted as an issue — should return `{"status": "success"}` for better coherence

---

## Key Takeaways

- Playwright tools + LangChain toolkit = agent that drives a real browser autonomously
- The graph structure is unchanged from Lab 2 — new capabilities come from richer tools
- `await tool.arun()` is the async equivalent of `tool.invoke()`
- Checkpointing replaces Gradio history — more robust and persistent
- Cost remains extremely low (~0.8¢) even with multiple browser interactions
- This is the foundation for the full **Sidekick project** — an agent that can do real web-based work for you

---

## Up Next

The full **Sidekick project** — multi-agent workflow with worker, evaluator, structured outputs, and Playwright — built as a proper Python application.