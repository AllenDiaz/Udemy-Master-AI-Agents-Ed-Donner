# MCP Lab 3 — Context Engineering: Long-Term Memory & Web Search

## Overview

This lesson covers **context engineering with MCP servers** — two powerful patterns: persistent long-term memory using a graph-based memory server, and free web search via Tavily.

---

## What Is Context Engineering?

Giving agents access to **persistent, external context** beyond the conversation window:
- Long-term memory that survives across sessions
- Real-time web search for current information

Both are implemented as MCP servers — no custom code needed.

---

## Pattern 1 — Long-Term Memory (Anthropic Memory Server)

### Setup

```python
memory_params = {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-memory"],
    "env": {"MEMORY_FILE_PATH": "./memory.json"}
}
```

### Available Tools

| Tool | Purpose |
|---|---|
| `create_entities` | Store named entities (people, concepts, things) |
| `create_relations` | Store relationships between entities (graph edges) |
| `add_observations` | Add facts/observations about an entity |
| `search_nodes` | Search the memory graph |
| `read_graph` | Read the full memory graph |

> Stores data as a lightweight **JSON graph database** (JSONL format) in `memory.json`.

### Storing Memories

```python
instructions = "Use your entity tools as a persistent memory to store and recall information."
request = "My name is Ed. I'm an LLM engineer teaching a course about AI agents including MCP."

async with MCPServerStdio(memory_params, timeout=60) as memory_mcp:
    agent = Agent(
        name="Memory Agent",
        instructions=instructions,
        model="gpt-4o-mini",
        mcp_servers=[memory_mcp]
    )
    result = await Runner.run(agent, request)
```

**What was stored in `memory.json`:**
- Entity: `Ed` (type: Person)
- Entity: `AI Agents Course` (type: Course)
- Entity: `MCP Protocol` (type: Concept)
- Relations: Ed → teaches → AI Agents Course → covers → MCP Protocol

### Recalling Memories (New Session)

```python
# Later conversation — agent recalls from persistent memory
result = await Runner.run(agent, "My name's Ed. What do you know about me?")
# → recalls Ed's role, the course, MCP — all from memory.json
```

**LangSmith trace showed:**
1. `list_tools` → discovered memory tools
2. `create_entities` → stored Ed, course, MCP
3. `create_relations` → linked entities
4. (Later) `search_nodes("Ed")` → recalled all stored facts

---

## Pattern 2 — Web Search (Tavily MCP Server)

### Setup

1. Sign up at [tavily.com](https://tavily.com) — free tier, no credit card required
2. Get API key: `tvly-XXXXXXXX`
3. Add to `.env`: `TAVILY_API_KEY=tvly-XXXXXXXX`
4. Reload `.env` in notebook

```python
tavily_params = {
    "command": "npx",
    "args": ["@tavily/mcp"],
    "env": {"TAVILY_API_KEY": os.getenv("TAVILY_API_KEY")}
}
```

### Available Tools (Full)

| Tool | Purpose |
|---|---|
| `tavily_search` | Search the web |
| `tavily_extract` | Extract content from a URL |
| `tavily_crawl` | Crawl a website following links |
| `tavily_map` | Map a website's link structure |
| `tavily_research` | Deep research across multiple sources |

### Filtering to One Tool

```python
from openai_agents_sdk.mcp import create_static_tool_filter

search_only = create_static_tool_filter(allowed_tool_names=["tavily_search"])

async with MCPServerStdio(tavily_params, timeout=60, tool_filter=search_only) as tavily_mcp:
    agent = Agent(
        name="Web Researcher",
        instructions=f"Search the web for information. Current date: {datetime.now()}",
        model="gpt-4o-mini",
        mcp_servers=[tavily_mcp]
    )
    result = await Runner.run(
        agent,
        "Research the latest news on Amazon stock price and summarize its outlook."
    )
```

> `create_static_tool_filter` limits which tools the agent can call — prevents unintended use of `tavily_crawl`, `tavily_research`, etc.

**LangSmith trace confirmed:**
- `tavily_search("Amazon stock price latest news")` was called
- Results returned → agent summarized the outlook accurately

---

## Tavily vs OpenAI Hosted Search

| | Tavily MCP | OpenAI WebSearchTool |
|---|---|---|
| Cost | **Free** (free tier) | $0.025 per call |
| Credit card | Not required | Not required |
| Setup | API key in `.env` | Already in OpenAI account |
| Quality | High | High |
| Tool filtering | `create_static_tool_filter` | N/A |

---

## Key Takeaways

- Long-term memory via MCP = persistent graph database, survives across sessions and kernel restarts
- Tavily is the free alternative to OpenAI's hosted web search — same quality, no per-call cost
- `create_static_tool_filter` controls which tools an agent can access — essential for focused agents
- Always inject `current date` into instructions for web search agents — prevents stale context
- Traces are essential to verify the agent actually searched vs. hallucinated

---

## Up Next

Day 4 — Agentic RAG with MCP servers.