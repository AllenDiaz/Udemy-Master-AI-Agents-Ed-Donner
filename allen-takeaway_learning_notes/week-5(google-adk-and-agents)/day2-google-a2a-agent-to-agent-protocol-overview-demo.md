# A2A (Agent-to-Agent Protocol) — Overview and Quick Demo

## Overview

This lesson covers **A2A** — Google's agent-to-agent communication protocol — including what it is, honest assessment of its current adoption, and a quick live demo using ADK Web.

---

## What Is A2A?

A2A is a **standard protocol for agents to discover, learn about, and communicate with each other**.

| Concept | Description |
|---|---|
| **Agent Card** | A JSON "business card" published at `/.well-known/agent.json` — describes an agent's capabilities |
| **Discovery** | Agents find each other via their agent cards |
| **Communication** | Standardized way for one agent to call another across platforms/frameworks |
| **Origin** | Announced by Google with major PR, then transferred to the Linux Foundation as open source |

### Complementary Framing

Google positioned A2A as a complement to MCP:
- **MCP** = connect agents to **tools**
- **A2A** = connect agents to **other agents**

---

## Honest Assessment of A2A Right Now

> *"A solution to a problem that isn't yet a major problem."*

| Point | Detail |
|---|---|
| Hype vs. adoption | Big launch, but marketplace activity is minimal ("crickets") |
| MCP overlap | MCP can already expose agents as tools — Firecrawl is an example |
| Prerequisite problem | We haven't yet solved basic agent architecture questions (single LLM vs. multiple, etc.) |
| Future potential | Could become essential when agents from different platforms need to collaborate at scale |
| Hacker News signal | MCP discussed constantly; A2A rarely mentioned |

> A2A may become very important as the industry matures — just not yet a pressing problem for most teams.

---

## A2A Demo — Quick Look

### Architecture

```
Spanish Concierge Agent (ADK Web, port 8000)
        │
        │ A2A call
        ▼
Translator Agent (A2A server, port 8001)
        │
        ▼
Returns Spanish translation
```

### Running the Demo

```bash
# Terminal 1 — Start the translator as an A2A service
cd week5/1_google_adk_a2a/a2a_demo
uv run translator_server.py   # exposes agent on port 8001

# Terminal 2 — View the agent card
curl http://localhost:8001/.well-known/agent.json
# or open in browser

# Terminal 3 — Launch ADK Web (from a2a_demo directory)
uv run adk web   # must be run from inside a2a_demo/
```

### The Agent Card (JSON)

```json
{
  "name": "Translator Agent",
  "description": "Translates English text into natural Spanish.",
  "capabilities": ["translate"]
}
```

> The agent card is like a business card — published at a well-known URL so other agents can discover capabilities.

### Result

Sent to Spanish Concierge: *"Please translate into Spanish: My favorite fruit is a banana."*

→ Spanish Concierge called Translator Agent via A2A → returned Spanish translation ✅

---

## A2A vs MCP — Key Difference

| | MCP | A2A |
|---|---|---|
| **Connects** | Agent ↔ Tools | Agent ↔ Agent |
| **Adoption** | Massive, widespread | Early, limited |
| **Overlap** | Can expose agents as MCP tools | Designed specifically for agent-to-agent |
| **Best for** | Tool integration | Cross-platform agent collaboration (future) |

---

## Key Takeaways

- A2A is a promising standard but adoption is still early — don't over-invest in it yet
- The "complement to MCP" framing has a catch — MCP already works for agent-to-tool-as-agent patterns
- ADK makes A2A easy — just a couple of calls to expose and consume agents
- The agent card at `/.well-known/agent.json` is the discovery mechanism
- Worth knowing about and watching — could become essential as multi-platform agent ecosystems mature

---

## Day 1 Recap — Google ADK + A2A

| Topic | Key Concept |
|---|---|
| LlmAgent | ADK's agent class — similar to OpenAI Agents SDK's `Agent` |
| Tools | Plain Python functions — no decorator needed |
| MCP | Plug in pre-built tool servers via config |
| Agent loop | Goal + to-do board + tools = agentic behavior |
| ADK Web | Local visual observability dashboard |
| A2A | Agent-to-agent discovery and communication protocol |

---

## Up Next

Day 2 — **Strands** (AWS) and **Pydantic AI**.