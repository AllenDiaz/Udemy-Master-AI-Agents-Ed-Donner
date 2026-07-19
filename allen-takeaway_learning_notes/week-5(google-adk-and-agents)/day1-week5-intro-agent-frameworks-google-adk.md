# Week 5 — Whirlwind Tour of Agent Frameworks & Google ADK Intro

## Overview

Week 5 is a fast-paced tour of **6.5 agent frameworks**, reinforcing the core insight that once you know one framework, you essentially know them all. Each lab follows the same 5 steps, and MCP is woven into every single one.

---

## The Big Message

> **Once you know one agent framework, you kind of know them all.**

They all do the same thing under the hood:
- Call tools in a loop to achieve a goal
- Same abstractions, different syntax and nuances
- Personal preference and team skills should drive your choice
- The "best" framework honestly doesn't matter that much

---

## Week 5 Schedule

| Day | Frameworks |
|---|---|
| Day 1 | **Google ADK** + A2A sidebar |
| Day 2 | **Strands** (AWS) + **Pydantic AI** |
| Day 3 | **Microsoft Agent Framework (MAF)** + **Agno** |
| Day 4 | **Mastra** (TypeScript — only TS in the course) |
| Day 5 | **Project: Agent Loop** — meta loop calling all agents from Days 1–4 |

---

## The 5 Steps Applied to Every Framework

Each lab this week follows the exact same structure:

| Step | What It Does | Analog |
|---|---|---|
| 1 | Create an agent with model + system prompt | `Agent` in OpenAI Agents SDK |
| 2 | Run it — send a message, get a reply | `Runner.run()` |
| 3 | Add tools — simple functions the agent can call | Tool calling |
| 4 | Add MCP | MCP integration |
| 5 | Put it in a loop with a goal | True agentic behavior |

> Steps 1–2 = LLM call in disguise. Steps 3–5 = where frameworks actually earn their keep.

---

## Agent Definition (Repeated for Emphasis)

> **An AI agent = an LLM in a loop with tools to achieve a goal.**

---

## Google ADK — Introduction

**Released:** April 2025  
**Current version:** 2.2+  
**Available in:** Python, TypeScript, and more

### Key Features

| Feature | Description |
|---|---|
| **Code-centric** | Just write a function — it becomes a tool, no decorators needed |
| **ADK Web** | Local observability playground (unique to ADK) |
| **MCP built-in** | First-class MCP support |
| **A2A built-in** | Agent-to-Agent standard — Google's own protocol, first-class citizen |
| **LiteLLM** | Flexible model support — not locked to Gemini |

### Compared to OpenAI Agents SDK

- Very similar overall — nearly direct parallels between constructs
- ADK feels slightly heavier — more plumbing to learn (ADK Web, A2A concepts)
- Lighter frameworks exist, but ADK is well-loved by developers for its code-first approach

### Downsides

- Slightly more overhead than some lighter frameworks
- Came out after OpenAI Agents SDK — later to market

---

## Key Takeaways

- All 6 frameworks this week are variations on the same theme — LLM + tools + loop
- MCP will be added to **every** framework this week — lots of MCP exposure before Week 6
- A2A (Agent-to-Agent) is Google's inter-agent communication protocol — a new standard to watch
- ADK Web is a unique local observability tool — no equivalent in other frameworks
- By the end of the week, you'll have a broad view of the ecosystem and can make informed framework choices

---

## Up Next

Google ADK in the lab — creating an agent, adding tools, connecting MCP, and running in a loop.