# Agno — Lightweight Agent Framework Introduction

## Overview

**Agno** (formerly Phidata) is a lightweight, fast, open-source Python agent framework — the last Python framework of Week 5 before the TypeScript detour with Mastra on Day 4.

---

## What Is Agno?

| Detail | Value |
|---|---|
| **Formerly known as** | Phidata |
| **Type** | Lightweight, open-source agent framework |
| **Startup time** | ~3 microseconds per agent — extremely fast |
| **Companion product** | AgentOS (paid runtime for deploying/scaling Agno agents) |
| **Maturity** | Reasonably mature (AgentOS recently revamped, Agno itself stable) |

---

## Key Features

| Feature | Detail |
|---|---|
| **Tools** | Plain Python functions — no decorator needed |
| **MCP** | Same pattern as other frameworks — tools passed as list |
| **Agent loop** | `agent.arun()` — async run (similar to LangChain's `ainvoke`) |
| **Startup speed** | Agent object is extremely lightweight — minimal overhead |
| **Model flexibility** | Swap models via `OpenAIChat` or other wrappers |
| **AgentOS** | Companion deployment/scaling runtime |

---

## Trade-offs

| ✅ Pros | ⚠️ Cons |
|---|---|
| Very lightweight and fast | Rename churn (V2 had breaking changes) |
| Simple, lean tools approach | AgentOS is a paid product (monetization pressure) |
| Mature framework | Free tier limited on AgentOS |
| Easy model swapping | |
| Built-in scaling via AgentOS | |

---

## Agno vs Other Frameworks This Week

| Framework | Unique differentiator |
|---|---|
| Google ADK | ADK Web local dashboard, A2A support |
| Pydantic AI | Type safety, native structured outputs |
| MAF | .NET support, LangGraph-like workflow engine |
| **Agno** | **Fastest startup (~3μs), lightest agent object** |

---

## Key Takeaways

- Agno's main value proposition: **speed and lightness** — agent creation is near-instant
- Tools are plain Python functions — same pattern as ADK, Pydantic AI, and MAF
- `agent.arun()` is the async run method — same concept, slightly different name
- AgentOS = the commercial companion for production deployment
- Still the same 5 steps — just different syntax and import names

---

## Up Next

Agno lab — the same 5 steps applied to Agno, then Day 4 with Mastra (TypeScript).