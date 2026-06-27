# LangGraph — Sidekick as a Python Module (tools.py & sidekick.py)

## Overview

This lesson converts the Sidekick from a notebook prototype into a proper Python application — a `tools.py` module with an expanding toolkit, and a `sidekick.py` class that encapsulates the full LangGraph workflow.

---

## `tools.py` — The Sidekick's Toolkit

### Available Tools

```python
from langchain_community.utilities import GoogleSerperAPIWrapper, WikipediaAPIWrapper
from langchain_community.agent_toolkits import FileManagementToolkit, PlaywrightBrowserToolkit
from langchain_experimental.tools import PythonREPLTool
from langchain.tools import Tool
```

| Tool | Source | Notes |
|---|---|---|
| `send_push_notification` | Custom (Pushover) | Homegrown tool |
| `file_tools` | `FileManagementToolkit` | Read/write files in a sandboxed directory |
| `search` | `GoogleSerperAPIWrapper` | Free SerpAPI web search |
| `wikipedia` | `WikipediaAPIWrapper` | Free Wikipedia lookup |
| `python_repl` | `PythonREPLTool` | Run Python code ⚠️ not sandboxed |
| `playwright_tools` | `PlaywrightBrowserToolkit` | Browser automation |

### ⚠️ Python REPL Warning

```python
# PythonREPLTool runs code directly on your machine — NOT in Docker
# Unlike CrewAI's code execution (Docker-sandboxed), this has no isolation
# Remove from tools list if uncomfortable:
other_tools = [push_tool, *file_tools, search_tool, wikipedia_tool]  # no python_repl
```

### Playwright Tools Setup

```python
async def get_playwright_tools():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    toolkit = PlaywrightBrowserToolkit.from_browser(async_browser=browser)
    tools = toolkit.get_tools()
    return tools, browser, playwright   # return browser + playwright for cleanup
```

> Return the browser and playwright objects so they can be properly closed when done.

### Extending the Toolkit

```python
# Just add more tools to other_tools — they're automatically available to the agent
other_tools = [push_tool, *file_tools, search_tool, wikipedia_tool, python_repl]
```

The LangChain ecosystem has many more tools available:
- Google Calendar integration
- Shell/terminal tools
- Email tools
- And many more in `langchain_community` and `langchain_experimental`

---

## `sidekick.py` — The Sidekick Class

### Why a Class?

Moving from notebook → Python module requires managing:
- Async initialization (Playwright can't be set up in `__init__`)
- Instance variables for LLMs, tools, graph, browser
- Clean resource teardown

### Class Structure

```python
class Sidekick:
    def __init__(self):
        # Sync init — no async allowed here
        self.graph = None
        self.browser = None
        self.playwright = None

    async def setup(self):
        # Async initialization — call this after __init__
        tools, self.browser, self.playwright = await get_playwright_tools()
        self.tools = tools + other_tools

        self.worker_llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(self.tools)
        self.evaluator_llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(EvaluatorOutput)

        self.build_graph()   # five steps — define state, nodes, edges, compile

    async def cleanup(self):
        await self.browser.close()
        await self.playwright.stop()
```

**Usage pattern:**
```python
sidekick = Sidekick()
await sidekick.setup()   # must be called before use
# ... use sidekick ...
await sidekick.cleanup()
```

---

## State and Schema (Same as Notebook)

```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
    success_criteria: Optional[str]
    feedback_on_work: Optional[str]
    success_criteria_met: bool
    user_input_needed: bool

class EvaluatorOutput(BaseModel):
    feedback: str
    """Feedback on the assistant's response"""
    success_criteria_met: bool
    """Whether the success criteria has been met"""
    user_input_needed: bool
    """True if the assistant needs user input or is stuck"""
```

---

## Notebook → Module Transition Philosophy

> Notebooks are ideal for AI engineering work — prompt iteration, experimentation, and prototyping.  
> Once prompts are refined and behavior is stable, move to a Python module for production use.

This is different from traditional TDD/software engineering — AI engineering is inherently more experimental by nature.

---

## Key Takeaways

- `tools.py` centralizes all tool definitions — add new tools in one place, instantly available to the agent
- The LangChain community ecosystem has a vast library of ready-to-use tools
- `PythonREPLTool` is powerful but unsandboxed — use with caution (unlike CrewAI's Docker execution)
- Async class initialization requires a separate `setup()` coroutine — `__init__` must stay synchronous
- Return `browser` and `playwright` from tool setup for proper resource cleanup
- The class structure mirrors the notebook exactly — just organized for production

---

## Up Next

Building the `build_graph()` method, the `run()` method, and the full Gradio UI entry point.