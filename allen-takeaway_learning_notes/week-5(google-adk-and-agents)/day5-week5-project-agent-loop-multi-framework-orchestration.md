# Week 5 Project — The Agent Loop (Multi-Framework Orchestration)

## Overview

The Week 5 capstone project — **The Agent Loop** — brings together all 6 frameworks in a single orchestrated system. A Google ADK orchestrator manages a team of agents (one per framework) that collaborate to build a language-learning website with mini-games.

---

## Week 5 Framework Recap — Key Differences

| Framework | Tool definition | Run method | Notable |
|---|---|---|---|
| OpenAI Agents SDK | Plain / `@function_tool` | `Runner.run()` | Guardrails, handoffs |
| Google ADK | Plain functions | `runner.run_async()` | `LlmAgent`, ADK Web, A2A |
| Strands | Decorator required | `agent()` | AWS-backed |
| Pydantic AI | Plain functions | `agent.run()` | Type safety, structured outputs |
| MAF | Plain functions | `agent.run()` | .NET support, LangGraph-like engine |
| Agno | Plain functions | `agent.arun()` | ~3μs startup, AgentOS |
| Mastra | `createTool()` + Zod | `agent.generate()` | TypeScript, Mastra Studio |

> **Core message:** You can do all of this without any framework. Frameworks are utility/abstraction code. Pick whichever fits your team best — the differences are minor.

---

## The Agent Loop Project

### Goal

User provides a **language** (e.g. Spanish) → team of agents builds a **language-learning website** with multiple mini-games, running locally.

---

## Architecture

```
User provides: target language
        │
        ▼
[Google ADK Orchestrator]
  - Sets overall goals on shared to-do board
  - Launches all builder agents in parallel
  - Monitors progress
  - Runs browser QA (Playwright via MCP)
  - Fixes bugs found during QA
        │
        ├── [Strands agent]      → builds mini-game 1
        ├── [Pydantic AI agent]  → builds mini-game 2
        ├── [MAF agent]          → builds mini-game 3
        ├── [Agno agent]         → builds mini-game 4
        └── [Mastra agent]       → builds mini-game 5
                │
                ▼
        All write progress to shared SQLite to-do board
```

---

## Nested Agent Loops

```
Outer loop: ADK Orchestrator
  → decides goals, assigns tasks, monitors board
        │
        ▼
  Inner loops: each builder agent
    → reads goal from board
    → plans sub-steps
    → builds the game
    → crosses off steps
    → reports completion
```

> The "magic" is just to-do list tools + token prediction. Each agent predicts tokens consistent with marking tasks complete, reading the next item, and taking action — that's all that's happening.

---

## Shared To-Do Board

All agents read and write to the **same SQLite database**:

```
[Goal] Build Spanish language website
  ├── [Strands]      Build vocabulary matching game    ✅
  ├── [Pydantic AI]  Build fill-in-the-blank game      ✅
  ├── [MAF]          Build word scramble game           ✅
  ├── [Agno]         Build pronunciation quiz           ✅
  └── [Mastra]       Build flashcard game               ✅
```

The board is the coordination mechanism — no A2A, no complex messaging protocol needed.

---

## Browser QA Agent

After builder agents complete their games:
- ADK orchestrator launches a **Playwright browser agent** (via MCP)
- Navigates to each game page
- Tests functionality visually
- Reports bugs → orchestrator fixes them directly

---

## Orchestrate with LLMs vs. Code

| Approach | When to use |
|---|---|
| **Orchestrate with LLMs** (this project) | When you want flexibility, autonomy, and the ability to scale to harder problems |
| **Orchestrate with code** (sequential calls) | When you want deterministic, reliable, predictable execution |

> This project uses LLM orchestration deliberately — to demonstrate the agent loop concept and allow flexible scaling. For simple sequential workflows, plain Python code is often better.

---

## Why Not A2A?

> *"If you've got agents as code that you've written calling other agents that you've also written, there's no role for A2A."*

A2A is for agents running on **different hardware written by different people** that need to discover each other. Here, you control all the code — just call agents as tools or via Python code.

---

## Key Takeaways

- All 6 frameworks run simultaneously, doing essentially the same thing
- The shared SQLite to-do board is the only coordination mechanism needed
- Nested loops (outer orchestrator + inner builder loops) create sophisticated behavior from simple tools
- Browser QA via Playwright MCP gives the orchestrator the ability to verify and repair
- Agent autonomy = LLMs predicting tokens consistent with tool use — nothing more magical than that
- LLM orchestration trades reliability for flexibility — both approaches are valid depending on the use case

---

## Up Next

Week 6 — **MCP (Model Context Protocol)**: deep dive into the protocol that's been appearing throughout the course.