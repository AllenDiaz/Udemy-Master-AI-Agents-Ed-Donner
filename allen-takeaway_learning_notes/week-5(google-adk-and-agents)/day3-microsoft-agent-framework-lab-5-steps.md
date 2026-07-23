# Microsoft Agent Framework (MAF) — Lab (5 Steps)

## Overview

This lesson walks through the 5 steps in **Microsoft Agent Framework (MAF)** — reinforcing the now-familiar pattern with MAF-specific syntax. Includes notebook quirks for Windows compatibility and a standalone `maf_worker.py` module.

---

## The 5 Steps in MAF

### Step 1 — Create an Agent

```python
from agent_framework import Agent

# Create model client
client = OpenAIChatClient(model="gpt-4o-mini")

# Create agent
agent = Agent(
    client=client,
    instructions="You are a concise friendly assistant."
)
```

**MAF-specific:** Uses a separate `client` object rather than passing the model string directly.

---

### Step 2 — Run the Agent

```python
response = await agent.run("Say hello in Spanish")
# → "Hola"
```

> `agent.run()` — same simple pattern as Pydantic AI and Strands.

---

### Step 3 — Add Tools

```python
def show_todos() -> str:
    """Show the current to-do list and status of all tasks."""
    return board.list_todos()

def plan_steps(steps: list[str]) -> str:
    """Plan and add steps to the to-do board."""
    return board.add_steps(steps)

def complete_task(task_id: int) -> str:
    """Mark a task as complete by its ID."""
    return board.complete(task_id)

board_agent = Agent(
    client=client,
    instructions="You manage a shared to-do board.",
    tools=[show_todos, plan_steps, complete_task]   # plain functions
)

response = await board_agent.run("What's on the board right now?")
```

---

### Step 4 — Add MCP

```python
from agent_framework import MCPStdioTool

params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "./task_worker/workspace"]
)

mcp_tools = MCPStdioTool(params)   # wraps MCP server as tool set

file_agent = Agent(
    client=client,
    instructions="You can read and write files in your workspace.",
    tools=[mcp_tools]
)

response = await file_agent.run("Read notes.txt and summarize it in one short sentence.")
```

> ⚠️ **Notebook Windows quirk:** `MCPStdioTool` requires subclassing in a notebook on Windows to avoid event loop errors. The `worker.py` module version is clean — no workaround needed.

---

### Step 5 — Agent in a Loop with a Goal

```python
worker = Agent(
    client=client,
    instructions="You are a careful worker. Take the pending goal from the board and complete it.",
    tools=[show_todos, plan_steps, complete_task, mcp_tools]
)

board.reset()
board.add_goal("Read notes.txt, translate to Spanish, write to spanish.txt")

response = await worker.run("Please work the pending goal on the board. Use all your tools.")
```

**What happened:**
1. `show_todos` → read pending goal
2. `plan_steps` → created sub-steps
3. MCP `read_file` → read `notes.txt`
4. MCP `write_file` → wrote `spanish.txt`
5. `complete_task` → crossed off all steps ✅

---

## Running as a Python Module

```bash
cd week5/3_maf_agno
uv run maf_worker.py
```

Output: Spanish translation written to `spanish.txt`, all to-do steps marked complete ✅

---

## Framework Comparison — Running Update

| Step | OpenAI Agents SDK | Google ADK | Pydantic AI | MAF |
|---|---|---|---|---|
| Agent class | `Agent` | `LlmAgent` | `Agent` | `Agent` |
| Model input | string | string | `provider:model` | `client` object |
| System prompt | `instructions` | `instruction` | `instructions` | `instructions` |
| Run | `Runner.run()` | `runner.run_async()` | `agent.run()` | `agent.run()` |
| Tools | plain / `@function_tool` | plain functions | plain functions | plain functions |
| MCP | toolset | `MCPToolset` | `MCPServerStdio` | `MCPStdioTool` |

---

## Key Takeaways

- MAF follows the exact same 5-step pattern — minimal learning curve if you know any other framework
- The only notable difference: model is wrapped in a `client` object before being passed to `Agent`
- Plain functions as tools — no decorator needed, same as ADK and Pydantic AI
- Windows notebook quirk for MCP — clean in `.py` modules
- MAF has sophisticated workflow functionality under the hood (LangGraph-like) — not covered this week
- Confirmed: **if you know one framework, you know them all**

---

## Up Next

**Agno** — another popular framework with its own unique flavor.