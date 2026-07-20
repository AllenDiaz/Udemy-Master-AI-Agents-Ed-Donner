# Google ADK — MCP, Agent Loop & ADK Web UI (Steps 4–5)

## Overview

This lesson completes the Google ADK five steps — adding MCP file system tools, running the agent in a loop with a goal, packaging it as a Python module, and exploring the unique **ADK Web** local observability dashboard.

---

## Step 4 — Add MCP (File System Tools)

MCP lets you plug in someone else's pre-built tools via configuration — no need to write them yourself.

```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# Configure the Anthropic filesystem MCP server
filesystem_mcp = MCPToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "./task_worker/workspace"]
    )
)

# Create agent with MCP tools
agent = LlmAgent(
    model="gemini-2.0-flash-lite",
    name="file_agent",
    instruction="You can read and write files to your workspace. Use your tools to do what's asked.",
    tools=[filesystem_mcp]   # all MCP tools included automatically
)
```

**What the filesystem MCP server provides:**
- Read file
- Write file
- List directory
- Create directory
- Move/delete file

> This is the whole point of MCP — Anthropic wrote these tools once, packaged them as an MCP server, and anyone can reuse them with one line of config. No custom functions needed.

---

## Step 5 — Agent in a Loop with a Goal

```python
from google.adk.runners import InMemoryRunner

# Setup board with goal
board.reset()
board.add_goal("Read notes.txt, translate its contents into Spanish, write to spanish.txt, and send a push notification with a summary.")

# Create full agent with all tools
agent = LlmAgent(
    model="gemini-2.0-flash-lite",
    name="worker",
    instruction="You are a careful worker with a shared to-do board. Take the pending goal and see it through.",
    tools=[show_todos, plan_steps, complete_task, send_push_notification, filesystem_mcp]
)

# Proper async run (not debug mode)
runner = InMemoryRunner(agent=agent)
session = await runner.session_service.create_session(user_id="user", session_id="session1")

async for event in runner.run_async(
    user_id="user",
    session_id="session1",
    new_message="Please work the pending goal on the board."
):
    pass  # process events
```

**What the agent did autonomously:**
1. Called `show_todos` → read the pending goal
2. Called `plan_steps` → broke goal into sub-steps
3. Called `list_directory` (MCP) → checked workspace
4. Called `read_file` (MCP) → read `notes.txt`
5. Called `write_file` (MCP) → wrote `spanish.txt`
6. Called `complete_task` → crossed off each step
7. Called `send_push_notification` → delivered summary ✅

---

## To-Do Board Structure

The SQLite board supports **goals with sub-steps**:

```
Goal: Read notes.txt, translate, write spanish.txt, send notification
  ├── Step 1: Read notes.txt          ✅
  ├── Step 2: Translate to Spanish    ✅
  ├── Step 3: Write spanish.txt       ✅
  └── Step 4: Send push notification  ✅
```

The agent autonomously creates steps under a goal and crosses them off — mirrors the Claude Code to-do list pattern from Week 1.

---

## Packaging as a Python Module — `worker.py`

Notebook → Python module workflow:

```bash
# Run the packaged worker
uv run worker.py

# Seed board only (reset + add goal, no execution)
uv run worker.py --seed-only
```

> Always prototype in notebooks, then package into `.py` modules for production use. Later this week, `worker.py` will be called by the meta-agent loop on Day 5.

---

## ADK Web — Local Observability Dashboard

Unique to Google ADK — a locally-hosted UI for monitoring agent runs:

```bash
# Launch ADK Web (from the day 1 folder)
uv run adk web
# → Opens at http://localhost:8000
```

**What you see:**
- Agent tool calls visualized as a live diagram
- Which tools were called and in what order
- Intermediate results and final response
- Support for multiple agents via dropdown selector

> No equivalent in OpenAI Agents SDK or CrewAI (without paid platform). LangSmith is the closest, but that's a separate service. ADK Web runs entirely locally.

---

## ADK vs Other Frameworks — Running the Agent

ADK requires slightly more plumbing than OpenAI Agents SDK:

```python
# OpenAI Agents SDK (simple)
result = await Runner.run(agent, "message")

# Google ADK (more steps)
runner = InMemoryRunner(agent=agent)
session = await runner.session_service.create_session(user_id="user", session_id="s1")
async for event in runner.run_async(user_id="user", session_id="s1", new_message="message"):
    pass
```

---

## Key Takeaways

- MCP = plug in pre-built tools from any provider via configuration — no custom code needed
- The filesystem MCP server from Anthropic gives file read/write/list capabilities instantly
- `run_debug()` is for development; `run_async()` is the proper async production runner
- The to-do board supports goals + sub-steps — agent autonomously breaks down and tracks work
- ADK Web is a killer feature — local, visual, real-time agent observability with zero extra setup
- ADK has slightly more runner plumbing than OpenAI Agents SDK — a minor but real trade-off
- Package working notebooks into `worker.py` — they'll be called by the Day 5 meta-agent

---

## Up Next

A2A (Agent-to-Agent) — Google's inter-agent communication protocol.