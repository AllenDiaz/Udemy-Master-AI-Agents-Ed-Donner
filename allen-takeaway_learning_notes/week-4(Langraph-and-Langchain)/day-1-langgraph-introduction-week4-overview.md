# Introduction to LangGraph — Week 4 Overview

## Overview

Week 4 introduces **LangGraph** — a framework from LangChain focused on building robust, resilient, and repeatable agentic workflows. This lesson clarifies the LangChain ecosystem and positions LangGraph as the modern agent-focused offering.

---

## The LangChain Ecosystem — Three Products

| Product | Purpose |
|---|---|
| **LangChain** | Original abstraction layer for LLM app development (RAG, prompt templates, memory, tool calling) |
| **LangGraph** | Graph-based framework for complex, stateful, resilient agent workflows |
| **LangSmith** | Monitoring and observability tooling for LangChain and LangGraph |

> These are separate products from the same company. LangGraph does **not** require LangChain — you can call LLMs directly or use any framework alongside it.

---

## LangChain — What It Is

- One of the earliest LLM abstraction frameworks
- Provides: RAG pipelines, prompt templates, memory management, tool abstractions, chaining LLM calls
- Abstracts away provider differences (swap GPT ↔ Claude with minimal code changes)
- Has its own declarative language (LCEL)

**Trade-off (similar to CrewAI):**
- ✅ Rapid development, battle-tested patterns, lots solved out of the box
- ❌ More opinionated, less visibility into actual prompts, signing up for "their way"

> As LLM APIs have converged on OpenAI's structure, the need for LangChain's abstractions has reduced for simpler use cases.

---

## LangGraph — What It Is

LangGraph is built around one core idea: **model any workflow as a graph**.

- **Nodes** = discrete steps or activities in the workflow
- **Edges** = connections and transitions between nodes
- **Graph** = the full picture of how an agentic workflow flows

### What LangGraph Solves

| Problem | LangGraph Solution |
|---|---|
| Unpredictable agent behavior | Structured graph enforces workflow boundaries |
| No human oversight | Human-in-the-loop support at any node |
| State loss between steps | Built-in memory and checkpointing |
| No recovery from failures | Fault-tolerant, scalable execution |
| Hard to debug | Connects to LangSmith for visibility |

### Key Features

- **Human-in-the-loop** — pause workflow for human approval/input at any node
- **Multi-agent collaboration** — multiple agents as nodes in the same graph
- **Memory** — conversation history and state persisted across steps
- **Time travel** — checkpoint system allows stepping backward to any prior state
- **Fault-tolerant scalability** — handles failures without crashing the whole workflow

---

## LangGraph vs. LangChain vs. CrewAI

| | LangChain | LangGraph | CrewAI |
|---|---|---|---|
| **Focus** | LLM app glue code | Stateful, resilient workflows | Autonomous agent teams |
| **Structure** | Chains / pipelines | Graphs (nodes + edges) | Crews (agents + tasks) |
| **Agent support** | Basic | Advanced | Advanced |
| **Human-in-loop** | Limited | First-class | Limited |
| **Observability** | LangSmith | LangSmith | CrewAI Enterprise |
| **Best for** | RAG, simple chains | Complex stateful flows | Autonomous collaboration |

---

## LangSmith — Observability

- Separate product that works with both LangChain and LangGraph
- Provides visibility into calls, reasoning, and failures
- Used this week to monitor LangGraph workflows in action

---

## Key Takeaways

- LangGraph ≠ LangChain — they're separate products from the same company
- LangGraph is the **modern, agent-focused** offering designed for today's agentic AI
- Its core abstraction is a **graph of nodes** — every workflow maps to this model
- Key differentiators: human-in-the-loop, time travel (checkpointing), fault tolerance
- LangGraph is the strongest choice for **production stateful workflows** requiring reliability
- Week 4 is shorter — core concepts carry over from OpenAI Agents SDK and CrewAI

---

## Up Next

Building real LangGraph workflows — nodes, edges, state, and agents in a graph.