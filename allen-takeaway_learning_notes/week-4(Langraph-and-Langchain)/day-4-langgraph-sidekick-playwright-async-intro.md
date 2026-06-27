# LangGraph — Sidekick Project Intro (Playwright Browser Tools & Async)

## Overview

Week 4 Day 4 kicks off the **Sidekick project** — a multi-agent LangGraph application powered by Playwright browser automation. This lesson introduces async LangGraph, the Playwright browser toolkit, and the `nest_asyncio` workaround for notebooks.

---

## What's New This Lesson

| Topic | Description |
|---|---|
| **Async LangGraph** | Running the graph with `await graph.ainvoke()` |
| **Playwright** | Browser automation tool — lets agents browse the web |
| **PlaywrightBrowserToolkit** | LangChain toolkit providing granular browser control tools |
| **Structured outputs** | Returning typed Pydantic objects from agent nodes |
| **Multi-agent workflow** | LangGraph equivalent of handoffs / crew of agents |

---

## Async LangGraph

```python
# Sync (previous lessons)
result = graph.invoke(state)
tool.run(inputs)

# Async (this lesson)
result = await graph.ainvoke(state)
await tool.arun(inputs)
```

Everything else stays the same — just add `await` and use the async variants.

---

## `nest_asyncio` — Notebook Workaround

Jupyter notebooks run their own event loop. `asyncio` doesn't allow a nested event loop by default — this causes errors when running async LangGraph inside a notebook.

```python
import nest_asyncio
nest_asyncio.apply()   # patches asyncio to allow nested event loops
```

> This is only needed in notebooks. In production Python code (`.py` files), it's not required.

---

## State (TypedDict)

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)
```

---

## Push Notification Tool (Reused)

```python
from langchain.tools import Tool

def push(message: str) -> str:
    """Send a push notification to the user."""
    # Pushover API call
    ...

tool_push = Tool(
    name="send_push_notification",
    func=push,
    description="Send a push notification to the user"
)
```

---

## Playwright — Browser Automation

**Playwright** (by Microsoft) is a modern browser automation framework — the successor to Selenium. Used for:
- Automated testing
- Web scraping (renders JavaScript, paints the full page)
- Agent-driven browsing

### Install

```bash
# Mac/Windows
playwright install

# Linux
playwright install --with-deps
```

**Two modes:**
- **Headless** — browser runs invisibly in the background
- **Headful** — browser window is visible and interactive

---

## PlaywrightBrowserToolkit

LangChain provides a toolkit that wraps Playwright into a set of agent-ready tools:

```python
from langchain_community.agent_toolkits import PlaywrightBrowserToolkit
from playwright.async_api import async_playwright

# Launch async browser
playwright = await async_playwright().start()
browser = await playwright.chromium.launch(headless=False)

# Build toolkit
toolkit = PlaywrightBrowserToolkit.from_browser(async_browser=browser)
tools = toolkit.get_tools()
```

### Available Tools

| Tool | Description |
|---|---|
| `click_element` | Click on a page element |
| `navigate_browser` | Go to a URL |
| `previous_webpage` | Go back (browser back button) |
| `extract_text` | Get text content from the current page |
| `extract_hyperlinks` | Get all links from the current page |
| `get_elements` | Get specific DOM elements |
| `current_webpage` | Get the current URL |

> These tools give the agent **granular, programmatic control** over a real browser window.

---

## Key Takeaways

- Async LangGraph = same patterns, just `await graph.ainvoke()` instead of `graph.invoke()`
- `nest_asyncio.apply()` is the quick fix for async in Jupyter — not needed in `.py` files
- Playwright gives agents the ability to **actually browse the web** — not just search APIs
- `PlaywrightBrowserToolkit` wraps all browser interactions as LangChain tools automatically
- This toolkit is far more powerful than a search API — the agent can navigate, click, read, and interact with any website

---

## Up Next

Wiring Playwright tools into a LangGraph agent node, adding structured outputs, and building the full multi-agent Sidekick workflow.