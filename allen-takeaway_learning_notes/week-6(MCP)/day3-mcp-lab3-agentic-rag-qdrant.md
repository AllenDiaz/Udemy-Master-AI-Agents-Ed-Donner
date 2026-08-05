# MCP Lab 3 — Agentic RAG with Qdrant MCP Server

## Overview

This lesson implements **Agentic RAG** — giving an agent the ability to store and retrieve information from a vector database using the **Qdrant MCP server**. No RAG pipeline to build — just parameters.

---

## What Is Agentic RAG?

| | Traditional RAG | Agentic RAG |
|---|---|---|
| **How retrieval happens** | Hardcoded pipeline | Agent decides when/what to retrieve |
| **Trigger** | Every query | Tool call — agent chooses |
| **Implementation** | Custom encoder + vector DB + retrieval code | MCP tool — agent just uses it |

**Agentic RAG** = equipping an agent with vector search/store as tools → it retrieves semantically relevant information on demand.

---

## Qdrant MCP Server

**Qdrant** is an open-source vector database (like Chroma). The MCP server wraps it with two simple tools.

```python
qdrant_params = {
    "command": "uvx",
    "args": [
        "mcp-server-qdrant",
        "--qdrant-path", "./memory/qdrant",
        "--collection-name", "knowledge"
    ]
}
```

- Python program → runs with `uvx`
- Runs **locally** — no API key needed
- Uses **HuggingFace `all-MiniLM-L6-v2`** for embeddings (runs locally)
- Stores data in `./memory/qdrant`

> ⚠️ Requires local model download — may not work on all setups. Skip if it fails; not needed for the rest of the week.

### Available Tools

| Tool | Purpose |
|---|---|
| `qdrant_store` | Store text with metadata as a vector embedding |
| `qdrant_find` | Find semantically similar content to a query |

---

## Step 1 — Research and Store

Use Tavily (web search) + Qdrant (vector store) together:

```python
async with MCPServerStdio(tavily_params, timeout=60) as tavily_mcp:
    async with MCPServerStdio(qdrant_params, timeout=60) as qdrant_mcp:

        researcher = Agent(
            name="Researcher",
            instructions="""You research topics on the web and build up a knowledge base
                           that you'll use later.""",
            model="gpt-4o-mini",
            mcp_servers=[tavily_mcp, qdrant_mcp]
        )

        result = await Runner.run(
            researcher,
            "Research the latest news on NVIDIA and store the key facts in your knowledge base."
        )
```

**LangSmith trace showed:**
1. `tavily_search("NVIDIA latest news")` → retrieved current articles
2. `qdrant_store(content=..., metadata=...)` × 2 → stored key facts as vectors

---

## Step 2 — Retrieve from Knowledge Base (No Internet)

Now query the stored knowledge — **no Tavily, no internet**:

```python
async with MCPServerStdio(qdrant_params, timeout=60) as qdrant_mcp:

    retriever = Agent(
        name="Retriever",
        instructions="Answer questions based on your knowledge base.",
        model="gpt-4o-mini",
        mcp_servers=[qdrant_mcp]   # Qdrant only — no web access
    )

    result = await Runner.run(
        retriever,
        "Based on your knowledge base, what's the latest information on NVIDIA?"
    )
```

**LangSmith trace showed:**
- `qdrant_find("NVIDIA latest news or updates")` → returned semantically matched stored content
- Agent answered using only retrieved knowledge ✅

---

## Why This Matters

**Without Qdrant MCP:**
- Build custom embedding pipeline
- Set up vector database
- Write retrieval and insertion code
- Handle encoder model loading
- ~1 week of work (see AI Engineering Core track)

**With Qdrant MCP:**
```python
qdrant_params = {"command": "uvx", "args": ["mcp-server-qdrant", ...]}
# Done. Agent has full RAG capability.
```

> This is MCP at its best: someone else built the RAG infrastructure, wrapped it in an MCP server, and you get it with just parameters.

---

## Key Takeaways

- Agentic RAG = the agent decides when to store/retrieve — triggered by tool calls
- Qdrant MCP server = `qdrant_store` + `qdrant_find` — that's the entire RAG pipeline
- Local embeddings via HuggingFace `all-MiniLM-L6-v2` — no external API needed
- Two-phase pattern: **research + store** → **retrieve + answer** (no internet on second pass)
- The power of MCP: complex infrastructure (vector DB, encoder model, RAG) → just parameters

---

## Day 3 Complete — Context Engineering Summary

| Pattern | MCP Server | What It Gives the Agent |
|---|---|---|
| Long-term memory | `@modelcontextprotocol/server-memory` | Persistent entity/relation graph |
| Web search | `@tavily/mcp` | Real-time internet search |
| Agentic RAG | `mcp-server-qdrant` | Vector store + semantic retrieval |

---

## Up Next

Day 4 — The Week 6 project: building a trading agent with MCP.