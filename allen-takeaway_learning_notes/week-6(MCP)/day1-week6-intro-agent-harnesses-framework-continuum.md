# Week 6 Intro — Agent Harnesses, Framework Continuum & MCP

## Overview

Week 6 opens with a recap of agents and agent frameworks, introducing the concept of an **agent harness** and placing all frameworks covered on a spectrum from lightweight to heavyweight — then setting the stage for MCP week.

---

## The Agent Harness

> **AI Agent = LLM + Harness**

| Component | What it is |
|---|---|
| **LLM** | The token predictor |
| **Harness** | Tools + loop to achieve a goal = everything else |

You can build a harness yourself (Week 1 — vanilla LLM calls + while loop) or use a framework to give you a head start.

---

## Agent Framework Continuum

Frameworks can be placed on a spectrum from **low-level/lightweight** (left) to **high-level/batteries included** (right):

```
← More work by you                    Less work by you →
← More control                        Less control →
← Easier to debug                     Harder to debug →

Direct    LangChain   LangGraph   Strands   OpenAI SDK    CrewAI    LangChain      Claude
LLM calls   Core                            ADK Agno              Create Agent   Agent SDK
                                            Mastra
                                            Pydantic AI
                                            MAF
```

### Placement Rationale

| Position | Frameworks | Reason |
|---|---|---|
| Far left | Direct LLM calls | No abstraction — you write everything |
| Left-center | LangChain Core, LangGraph | Low-level, you describe the graph/workflow |
| Center-left | Strands | Lightest of the whirlwind tour frameworks |
| Center | OpenAI SDK, ADK, Agno, Mastra, Pydantic AI, MAF | Similar level — hard to separate |
| Center-right | CrewAI | More opinionated, more happening in the framework |
| Right | LangChain Create Agent | High-level, gives you an agent loop out of the box |
| Far right | Claude Agent SDK | All-in harness — not really an agent framework |

---

## Claude Agent SDK — The Odd One Out

| Detail | Value |
|---|---|
| **What it is** | Programmatic interface to Claude Code |
| **Language** | Python + TypeScript |
| **Key function** | `query()` — iterate over Claude Code responses |
| **Built-in tools** | Read files, run commands, edit code, search web |
| **Model flexibility** | ❌ Claude only — cannot swap models |
| **Course coverage** | Not covered here — see AI Coder course |

> Not really an agent framework — more a way to drive Claude Code programmatically. The odd one out on the spectrum.

---

## Choosing Where on the Continuum

| If you want... | Use... |
|---|---|
| Full control, easy debugging | Left side (direct calls, LangGraph) |
| Balance of ease and control | Center (OpenAI SDK, Pydantic AI, Agno) |
| Quick results, less coding | Right side (CrewAI, LangChain Create Agent) |
| TypeScript ecosystem | Mastra |
| .NET support | MAF |
| Best developer tooling | ADK (ADK Web) or Mastra (Studio) |

> Personal preference: lean toward the left — more control, easier to debug when things go wrong.

---

## Key Takeaways

- An **agent harness** = tools + loop — what turns an LLM into an agent
- All frameworks sit on a continuum — not a binary "framework vs. no framework"
- More heavyweight frameworks = less code written, but less visibility into what's happening
- Claude Agent SDK is deliberately excluded — it's not a general framework, it's a Claude Code driver
- Week 1 and Week 2 are foundational — they explain *why* frameworks exist and *how* they work under the hood

---

## Up Next

**MCP (Model Context Protocol)** — the deep dive that's been teased throughout the entire course. Week 6, the instructor's favorite.