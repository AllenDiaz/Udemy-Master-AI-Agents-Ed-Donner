# MCP Lab 1 — Equipping an Agent with MCP Servers (Full Example)

## Overview

This lesson wires MCP servers into a real OpenAI Agents SDK agent — giving it Playwright (browser) and Filesystem tools — then demonstrates a remote MCP server (Context7) for live API documentation lookup.

---

## Identifying Host, Client, Server in Code

```python
async with MCPServerStdio(filesystem_params, timeout=60) as mcp_files:
    async with MCPServerStdio(playwright_params, timeout=60) as mcp_browser:
        agent = Agent(...)
```

| MCP Component | What it is here |
|---|---|
| **MCP Host** | The Jupyter Notebook / Python kernel running the agent |
| **MCP Client** | Created automatically by OpenAI Agents SDK (`MCPServerStdio`) |
| **MCP Server** | The process spawned by `uvx` or `npx` — running on your computer |

> Nobody writes MCP clients anymore — every agent framework creates them for you.

---

## Full Agent with Two MCP Servers

```python
from openai_agents_sdk import Agent, Runner
from openai_agents_sdk.mcp import MCPServerStdio

instructions = """
You browse the internet to accomplish your instructions.
Accept cookies, navigate pop-ups as needed.
If one website doesn't work, try another. Be persistent.
Write files inside the sandbox folder only.
"""

task = "Find a great recipe for banoffee pie, then summarize it in markdown to banoffee.md"

async with MCPServerStdio(filesystem_params, timeout=60) as mcp_files:
    async with MCPServerStdio(playwright_params, timeout=60) as mcp_browser:

        agent = Agent(
            name="Web Researcher",
            instructions=instructions,
            model="gpt-4o-mini",
            mcp_servers=[mcp_files, mcp_browser]   # both MCP servers
        )

        result = await Runner.run(agent, task, max_turns=20)
```

**What the agent did autonomously:**
1. Used Playwright to navigate to `bbcgoodfood.com`
2. Accepted cookie consent
3. Read recipe page content
4. Navigated between pages for more details
5. Used filesystem tool to write `sandbox/banoffee.md` ✅

---

## Traces in LangSmith / OpenAI Traces

After running, the trace showed every tool call:
- `list_mcp_tools` → discovered available tools
- `find_allowed_directories` → checked sandbox constraints
- `navigate_browser` → went to recipe website
- `take_snapshot` (×3) → captured page states
- `click` → interacted with page elements
- `write_file` → saved the markdown recipe

> **Always dig into traces** — they reveal exactly what the agent was doing and why, tool call by tool call.

---

## Remote MCP Server — Context7 (Streamable HTTP)

For remote MCP servers, use `MCPServerStreamableHTTP` instead of `MCPServerStdio`:

```python
from openai_agents_sdk.mcp import MCPServerStreamableHTTP

context7_params = {
    "url": "https://mcp.context7.com/mcp",
    "timeout": 30
}

async with MCPServerStreamableHTTP(context7_params) as mcp_context7:
    agent = Agent(
        name="API Researcher",
        model="gpt-4o-mini",   # old model — doesn't know recent APIs
        mcp_servers=[mcp_context7]
    )

    result = await Runner.run(
        agent,
        "The sandbox agents feature was added to OpenAI Agents SDK. What is the manifest object for? Be accurate and don't guess."
    )
```

**What Context7 provided:**
1. `resolve_library_id("openai-agents-sdk")` → found matching library
2. `query_docs("what is the manifest object?")` → returned current documentation
3. Old model answered accurately using fresh docs ✅

---

## STDIO vs Streamable HTTP — In Code

| Scenario | Class to use |
|---|---|
| Local MCP server (Python/Node) | `MCPServerStdio(params, timeout=60)` |
| Remote MCP server (URL) | `MCPServerStreamableHTTP(params)` |

---

## Key Takeaways

- MCP servers are passed to an agent via `mcp_servers=[...]` — framework handles client creation
- `timeout=60` is essential for first-run package downloads
- The context manager (`async with`) keeps MCP servers alive for the duration of the agent run
- `max_turns=20` gives the agent more steps for complex multi-tool tasks
- Context7 is the go-to remote MCP server for current API documentation
- Traces are invaluable — they show every tool call, what was sent, and what came back

---

## Day 1 Wrap-Up — MCP Covered So Far

| Concept | Status |
|---|---|
| What MCP is (protocol/standard) | ✅ |
| Host / Client / Server | ✅ |
| STDIO vs Streamable HTTP | ✅ |
| `uvx` vs `npx` launchers | ✅ |
| Local vs remote servers | ✅ |
| `list_tools` and `call_tool` | ✅ |
| MCP in an agent (OpenAI SDK) | ✅ |

---

## Up Next

Day 2 — Building your own MCP server from scratch.