# Google ADK Lab — Agent, Tools, and MCP (Steps 1–4)

## Overview

This lesson walks through the first four of five steps in the Google ADK framework — creating an agent, running it, adding tools, and connecting MCP. Uses a persistent SQLite to-do board as the running example.

---

## Setup Notes

- Requires **Node.js** — verify with `node --version`
- Uses **Gemini** by default (Google AI Studio API key in `.env`)
- Alternative models available via `swapai.md` instructions in each day's folder
- Pre-install MCP server: run the `npx` command in the lab to cache the package

---

## Step 1 — Create an Agent

```python
from google.adk.agents import LlmAgent

agent = LlmAgent(
    model="gemini-2.0-flash-lite",   # or any Gemini model
    name="my_agent",
    instruction="You are a concise friendly assistant. Reply in a single short sentence."
)
```

**ADK vs OpenAI Agents SDK:**

| | OpenAI Agents SDK | Google ADK |
|---|---|---|
| Class name | `Agent` | `LlmAgent` |
| System prompt field | `instructions` (plural) | `instruction` (singular) |
| Runner | `Runner` | `InMemoryRunner` (and others) |

---

## Step 2 — Run the Agent

```python
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(agent=agent)

# Run with debug output (easier for development)
response = await runner.run_debug("Say hello in Spanish")
# → "Hola"
```

> At this point it's just an LLM call — "agent in name only." Tools are what make it agentic.

---

## Step 3 — Add Tools

### The To-Do Board (SQLite-backed)

A persistent to-do list stored in SQLite — shared across agents later in the week.

```python
# Board functions (already implemented in board.py)
reset_board()           # clear all todos
add_goal(description)   # add a new task
list_todos()            # returns list of dicts
```

### Tools Are Just Python Functions

No decorators required in ADK — just type hints and a docstring:

```python
def show_todos() -> str:
    """Show the current to-do list and status of all tasks."""
    return board.list_todos()

def plan_steps(steps: list[str]) -> str:
    """Plan and add a list of steps to the to-do board."""
    return board.add_steps(steps)

def complete_task(task_id: int) -> str:
    """Mark a task as complete by its ID."""
    return board.complete(task_id)
```

### Attach Tools to Agent

```python
agent = LlmAgent(
    model="gemini-2.0-flash-lite",
    name="todo_agent",
    instruction="You help manage a to-do board.",
    tools=[show_todos, plan_steps, complete_task]   # plain functions
)
```

> ADK automatically generates the JSON schema from type hints and docstrings — no manual JSON required.

### Push Notification Tool

```python
def send_push_notification(message: str) -> str:
    """Send a push notification to the user."""
    # Pushover API call
    ...
    return "Notification sent."
```

Add to `tools=[]` alongside board tools.

---

## The To-Do Board in Action

```python
# Setup
board.reset()
board.add_goal("Read notes.txt, translate to Spanish, write to spanish.txt")

# Agent call
response = await runner.run_debug("What's on the board right now?")
# → Agent calls show_todos tool
# → "The board has 1 pending task: Read notes.txt, translate..."
```

---

## Key ADK Highlights So Far

| Feature | Detail |
|---|---|
| Tools | Plain Python functions — no decorator needed |
| Schema generation | Automatic from type hints + docstrings |
| Runner | `InMemoryRunner` for development |
| Debug mode | `run_debug()` for easier development output |
| Persistent state | SQLite to-do board shared across agents |

---

## Key Takeaways

- ADK is code-first — functions become tools with zero boilerplate
- `instruction` (singular) vs `instructions` (plural) — minor ADK quirk vs OpenAI SDK
- `InMemoryRunner` is the development runner — other runners available for production
- The SQLite to-do board persists across agents — sets up for the multi-agent project later
- Tools in ADK = plain Python functions with type hints and docstrings

---

## Up Next

Step 4 — Adding MCP to the Google ADK agent, and Step 5 — running the agent in a loop with a goal.