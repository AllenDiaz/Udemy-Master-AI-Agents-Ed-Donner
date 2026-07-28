# Agno — Lab (5 Steps)

## Overview

The final Python framework lab of Week 5 — same 5 steps, Agno syntax. The point is now well established: **all these frameworks are essentially the same thing.**

---

## The 5 Steps in Agno

### Step 1 — Create an Agent

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

model = OpenAIChat(id="gpt-4o-mini")

agent = Agent(
    model=model,
    instructions="You are a concise friendly assistant."
)
```

---

### Step 2 — Run the Agent

```python
response = await agent.arun("Say hello in Spanish")
# → "Hola"
```

> `agent.arun()` — async run. Note: not `run`, not `run_async`, not `ainvoke` — just `arun`.

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
    model=model,
    instructions="You manage a shared to-do board.",
    tools=[show_todos, plan_steps]   # plain functions, no decorator
)

response = await board_agent.arun("What's on the board right now?")
```

---

### Step 4 — Add MCP

```python
# Notebook Windows workaround (not needed in .py modules)
with MCPTools(params, timeout=60) as file_system:
    file_agent = Agent(
        model=model,
        instructions="You can read and write files in your workspace.",
        tools=[file_system]
    )
    response = await file_agent.arun("Read notes.txt and summarize it in one short sentence.")
```

> Context manager pattern for MCP in Agno — slightly different from other frameworks but same concept.

---

### Step 5 — Agent in a Loop with a Goal

```python
with MCPTools(params, timeout=60) as file_system:
    worker = Agent(
        model=model,
        instructions="You are a worker with a shared to-do board and file tools. Complete the pending goal.",
        tools=[show_todos, plan_steps, complete_task, file_system]
    )

    board.reset()
    board.add_goal("Read notes.txt, translate to Spanish, write to spanish.txt")

    response = await worker.arun("Please work the pending goal on the board.")
```

**What happened:**
1. `show_todos` → read goal from board
2. `plan_steps` → broke into 4 sub-steps (agent chose its own breakdown)
3. MCP `read_file` → read `notes.txt`
4. MCP `write_file` → wrote `spanish.txt`
5. `complete_task` → crossed off all steps ✅

---

## Running as a Python Module

```bash
cd week5/3_maf_agno
uv run agno_worker.py
```

Output: `spanish.txt` written, all to-do steps marked complete ✅

---

## Complete Framework Comparison — Week 5

| Step | OpenAI SDK | Google ADK | Pydantic AI | MAF | Agno |
|---|---|---|---|---|---|
| Agent class | `Agent` | `LlmAgent` | `Agent` | `Agent` | `Agent` |
| Model input | string | string | `provider:model` | `client` object | `OpenAIChat(id=)` |
| System prompt | `instructions` | `instruction` | `instructions` | `instructions` | `instructions` |
| Run | `Runner.run()` | `runner.run_async()` | `agent.run()` | `agent.run()` | `agent.arun()` |
| Tools | plain/decorated | plain functions | plain functions | plain functions | plain functions |
| MCP | toolset | `MCPToolset` | `MCPServerStdio` | `MCPStdioTool` | `MCPTools` context |
| Unique feature | Guardrails, handoffs | ADK Web, A2A | Type safety | .NET support | ~3μs startup |

---

## Key Takeaways

- Agno follows the exact same 5-step pattern with minimal syntax differences
- `agent.arun()` is Agno's async run — the only real naming difference
- MCP uses a context manager (`with MCPTools(...) as fs`) — slightly different pattern
- The agent autonomously decided on 4 sub-steps vs 3 in other runs — expected autonomous behavior
- **These labs are your cookbook** — copy-paste the relevant lab when you need any framework
- Your coding agent can fill in the framework-specific syntax — you just need to know the pattern

---

## Up Next

Day 4 — **Mastra** (TypeScript) — same 5 steps but finally something different!