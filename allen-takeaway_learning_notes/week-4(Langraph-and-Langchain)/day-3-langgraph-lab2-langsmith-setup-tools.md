# LangGraph Lab 2 — LangSmith Setup and Tools

## Overview

This lesson sets up **LangSmith** for observability and builds two tools for the LangGraph agent — a web search tool (SerpAPI via LangChain) and a custom push notification tool — using LangChain's `Tool` wrapper.

---

## LangSmith Setup

LangSmith is a free observability platform for monitoring LangGraph and LangChain runs.

### Steps

1. Create a free account at [smith.langchain.com](https://smith.langchain.com)
2. Press **"Setup Tracing"** on the dashboard
3. Generate an API key
4. Add to `.env`:

```bash
LANGCHAIN_API_KEY=your_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=mastering-agents   # or any project name
```

5. Run `load_dotenv(override=True)` to load the variables

### What You See in LangSmith

| Column | Description |
|---|---|
| Input / Output | Full message content per invocation |
| Latency | How long each run took |
| Cost | API cost per call (often fractions of a cent) |
| Tokens | Token usage per call |
| Errors | Failed runs with stack traces |

> Cost insight: Individual LangGraph invocations are extremely cheap — fractions of a cent. Costs only become significant at scale.

---

## Building Tools with LangChain's `Tool` Wrapper

LangChain provides a `Tool` object that wraps any Python function into a tool — handling the JSON schema generation automatically.

### Syntax

```python
from langchain.tools import Tool

tool = Tool(
    name="tool_name",
    func=my_function,
    description="What this tool does"
)

# Call it
tool.invoke("input string")
```

---

## Tool 1 — Web Search (SerpAPI via LangChain)

```python
from langchain_community.utilities import GoogleSerperAPIWrapper

serper = GoogleSerperAPIWrapper()   # uses SERPER_API_KEY from .env

tool_search = Tool(
    name="search",
    func=serper.run,
    description="Search the internet for current information"
)

# Test it
tool_search.invoke("What's the capital of France?")
# → "Paris is the capital and largest city of France..."
```

> `GoogleSerperAPIWrapper` is a convenient LangChain wrapper around the SerpAPI — same free credits, no per-call charges unlike OpenAI's hosted search tool.

---

## Tool 2 — Custom Push Notification

```python
import requests, os

def push(message: str) -> str:
    """Send a push notification to the user via Pushover."""
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": os.environ["PUSHOVER_TOKEN"],
        "user": os.environ["PUSHOVER_USER"],
        "message": message
    })
    return "Push notification sent."

tool_push = Tool(
    name="send_push_notification",
    func=push,
    description="Send a push notification to the user"
)

# Test it
tool_push.invoke("Hello!")   # → notification received on phone
```

---

## Tools List

```python
tools = [tool_search, tool_push]
```

Both tools are now ready to be attached to a LangGraph agent node.

---

## Key Takeaways

- LangSmith requires just 3 env variables — zero code changes to enable tracing
- LangChain's `Tool` wrapper eliminates the need to write JSON schemas manually
- `tool.invoke("input")` is the standard way to call a LangChain tool
- The docstring on a custom function becomes the tool description — write it clearly
- `GoogleSerperAPIWrapper` = free SerpAPI calls via LangChain (same API key as CrewAI's SerperDevTool)
- Tools defined here will be wired into the LangGraph agent in the next step

---

## Up Next

Wiring tools into a LangGraph node using `bind_tools()` and implementing the full agent loop with tool calling and checkpointing.