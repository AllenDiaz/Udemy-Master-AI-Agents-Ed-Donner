# Pydantic AI — Agent Framework (5 Steps)

## Overview

Pydantic AI is an agent framework from the team behind Pydantic — one of the **earliest** agent frameworks, and a partial inspiration for OpenAI Agents SDK. It's loved by engineers for its strong typing, clean API, and built-in structured output support.

---

## Key Facts

| Detail | Value |
|---|---|
| **Origin** | Pydantic team (partly inspired OpenAI Agents SDK) |
| **Released** | Beta 2024, stable release alongside other frameworks |
| **Current** | V1 stable, V2 in beta (minor breaking changes possible) |
| **Default model** | OpenAI (switchable via provider string) |
| **Observability** | LogFire (Pydantic's platform — not covered this week) |

---

## Key Features

- Strong Pydantic typing woven throughout
- **Structured outputs** — native and effortless (as expected from the Pydantic team)
- Flexible tool definitions — decorators available but not required
- MCP support similar to ADK
- `agent.run()` — clean, simple execution API

## Trade-offs

| ✅ Pros | ⚠️ Cons |
|---|---|
| Type safety built-in | No built-in orchestration (no `create_react_agent` equivalent) |
| Easiest structured outputs | V2 in beta — potential breaking changes |
| Flexible tool approach | LogFire requires separate setup |
| Clean, minimal API | |

---

## The 5 Steps in Pydantic AI

### Step 1 — Create an Agent

```python
from pydantic_ai import Agent

model = "openai:gpt-4o-mini"   # provider:model-name syntax

agent = Agent(
    model=model,
    instructions="You are a concise friendly assistant. Reply in a single short sentence."
)
```

> Uses `instructions` (plural) — same as OpenAI Agents SDK.  
> Model string uses `provider:model` format — same as LangChain/LiteLLM.

---

### Step 2 — Run the Agent

```python
result = await agent.run("Say hello in Spanish")
# → "Hola"
```

> `agent.run()` — simplest execution API of all frameworks covered this week.

---

### Step 3 — Add Tools

No decorator required — plain functions work just like ADK:

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

# Attach tools to agent
agent = Agent(
    model=model,
    instructions="You manage a shared to-do board.",
    tools=[show_todos, plan_steps, complete_task]   # plain functions
)
```

---

### Step 4 — Add MCP

```python
from pydantic_ai.mcp import MCPServerStdio

filesystem_mcp = MCPServerStdio(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "./task_worker/workspace"],
    init_timeout=10
)

agent = Agent(
    model=model,
    instructions="You can read and write files in your workspace.",
    tool_sets=[filesystem_mcp]   # note: tool_sets, not tools
)

result = await agent.run("Read notes.txt and summarize it in one short sentence.")
```

**Minor syntax differences vs ADK:**
- `MCPServerStdio` (capitalized) vs ADK's `StdioServerParameters`
- `init_timeout` vs `timeout`
- `tool_sets=[]` for MCP vs `tools=[]` for functions

---

### Step 5 — Agent in a Loop with a Goal

```python
worker = Agent(
    model=model,
    instructions="You are a careful worker. Take the pending goal from the board and complete it.",
    tools=[show_todos, plan_steps, complete_task],
    tool_sets=[filesystem_mcp]
)

board.reset()
board.add_goal("Read notes.txt, translate to Spanish, write to spanish.txt")

result = await worker.run("Please work the goal on your board.")
```

**What happened:**
1. `show_todos` → read the goal from the board
2. `plan_steps` → created 4 sub-steps
3. MCP `read_file` → read `notes.txt`
4. MCP `write_file` → wrote `spanish.txt`
5. `complete_task` → crossed off each step ✅

---

## Framework Comparison — Week 5 Syntax

| Step | OpenAI Agents SDK | Google ADK | Pydantic AI |
|---|---|---|---|
| Agent class | `Agent` | `LlmAgent` | `Agent` |
| System prompt | `instructions` | `instruction` | `instructions` |
| Run | `Runner.run()` | `runner.run_async()` | `agent.run()` |
| Tools | `@function_tool` or plain | Plain functions | Plain functions |
| MCP | Via toolset | `MCPToolset` | `MCPServerStdio` |
| Structured output | `output_type=` | Native | Native (Pydantic) |

---

## Key Takeaways

- Pydantic AI is clean, minimal, and type-safe — feels very Pythonic
- `agent.run()` is arguably the simplest execution API of any framework this week
- Tools don't require decorators — plain functions work just like ADK
- MCP syntax is slightly different but follows the same pattern
- Structured outputs are a first-class citizen — expected from the Pydantic team
- No built-in orchestration layer — you manage the loop yourself

---

## Up Next

Day 3 — **Microsoft Agent Framework (MAF)** and **Agno**.