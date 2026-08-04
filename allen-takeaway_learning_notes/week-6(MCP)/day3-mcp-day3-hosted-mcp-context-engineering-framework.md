# MCP Day 3 — Hosted MCP & Context Engineering Framework

## Overview

This lesson introduces the **4th MCP pattern (Hosted MCP)**, explains why to avoid it, and frames **context engineering** — the broader discipline of maximizing what goes into an LLM's context window.

---

## The 4th MCP Pattern — Hosted MCP (Avoid)

> Also called "managed MCP" — OpenAI runs the MCP client and server on their infrastructure during inference.

```
Your code → OpenAI API → [OpenAI runs MCP client + server] → tool result
```

### Why to Avoid It

| Issue | Detail |
|---|---|
| **Vendor lock-in** | Only works with OpenAI models — can't swap to Claude, Gemini, etc. |
| **Proprietary API** | Uses OpenAI's Responses API, not the standard completions endpoint |
| **Cost** | May incur additional charges |
| **Unnecessary** | STDIO/HTTP patterns work just as well without the lock-in |

> OpenAI lists this first in their MCP docs — but it should be your **last** choice, not first.

### Recommended Priority Order

```
1. STDIO (local server)          ← most common, most flexible
2. Streamable HTTP (remote)      ← for third-party services
3. Remote MCP (authenticated)    ← for paid products like Jira
4. Hosted MCP                    ← avoid — vendor lock-in
```

---

## Context Engineering

> **Context engineering** = the series of decisions you make to ensure the LLM's input contains the best possible information, tools, and resources for success.

Evolved from "prompt engineering" — a broader, more holistic concept.

### The Five Components (Phil Schmidt / Google DeepMind)

```
┌─────────────────────────────────────────────┐
│                 LLM Context                  │
│                                              │
│  ┌──────────────┐    ┌───────────────────┐  │
│  │ Instructions │    │  Short-term Memory │  │
│  │ (system      │    │  (conversation     │  │
│  │  prompt)     │    │   history)         │  │
│  └──────────────┘    └───────────────────┘  │
│                                              │
│  ┌──────────────┐    ┌───────────────────┐  │
│  │  Long-term   │    │   Tools (+ their  │  │
│  │  Memory /RAG │    │   results)         │  │
│  │  (databases) │    │                   │  │
│  └──────────────┘    └───────────────────┘  │
│                                              │
│         ┌───────────────────┐               │
│         │ Structured Output │               │
│         └───────────────────┘               │
└─────────────────────────────────────────────┘
```

### Component Breakdown

| Component | Description | Example |
|---|---|---|
| **Instructions** | System prompt — quality matters most | Clear, specific, well-tested prompts |
| **Short-term memory** | Conversation history — can be pruned/summarized | Summarize messages >1 hour old |
| **Long-term memory** | External database lookup for relevant context | Memory MCP server (yesterday's lab) |
| **RAG** | Semantic/vector search for meaning-based retrieval | Embed + search relevant documents |
| **Tools** | All equipped tools + their results | MCP servers, function tools |
| **Structured outputs** | Typed responses for downstream processing | Pydantic schemas |

### Overlapping Concepts

- RAG results often go into the system prompt
- Long-term memory and RAG are closely related
- **Agentic RAG** = using tools to trigger RAG retrieval — coming up next in the lab

---

## Key Takeaways

- Hosted MCP = vendor lock-in to OpenAI — use STDIO/HTTP instead
- Context engineering = everything about what you put into the LLM's input context
- Short-term memory = conversation history (with smart pruning)
- Long-term memory = external database access (memory MCP server)
- RAG = semantic search over external knowledge
- Agentic RAG = the agent decides when and what to retrieve using tools

---

## Up Next

Agentic RAG in practice — implementing semantic search as an MCP tool.