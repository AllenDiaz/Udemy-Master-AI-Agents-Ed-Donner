# CrewAI Day 2 — Tools, Context, and the Financial Researcher Crew

## Overview

Day 2 of Week 3 goes deeper into CrewAI by introducing two new concepts: **tools** (equipping agents with capabilities) and **context** (passing information between tasks). A new project — the **financial researcher crew** — is built to demonstrate both.

---

## Quick Recap: CrewAI Project Setup (5 Steps)

1. `crewai create crew <project_name>` — scaffolds the full directory structure
2. Edit `config/agents.yaml` — define agent roles, goals, backstories, and LLMs
3. Edit `config/tasks.yaml` — define task descriptions, expected outputs, agents, and output files
4. Edit `crew.py` — create agents, tasks, and the crew using decorators; reference YAML config
5. Edit `main.py` — set runtime inputs and call `crew.kickoff(inputs={...})`

Run with:
```bash
crewai run
```

---

## Two New Concepts This Lesson

### 1. Tools

Equipping CrewAI agents with external capabilities — same concept as in OpenAI Agents SDK, implemented the CrewAI way.

### 2. Context

How to explicitly pass the **output of one task as input to another task** — a key concept with no direct analog covered previously.

---

## New API: SerpAPI (Free Google Search)

The financial researcher crew uses **SerpDev** to run Google searches from code.

- Sign up at `serper.dev` — **2,500 free credits** (more than enough for this course)
- Get your API key from the dashboard
- Add to `.env`:

```bash
SERPER_API_KEY=your_key_here
```

> Note: Use `SERPER_API_KEY` — not to be confused with the similarly named `SERPAPI_API_KEY` from a different service.

**Why SerpDev over OpenAI's hosted web search tool?**

| | OpenAI Web Search Tool | SerpDev |
|---|---|---|
| Cost | ~$0.025/call | Free (2,500 credits) |
| Setup | None (hosted) | API key in `.env` |
| Flexibility | OpenAI only | Works with any framework |

---

## Scaffolding the Financial Researcher Crew

```bash
cd week3/crew
crewai create crew financial_researcher
```

Choose:
- Provider: `openai`
- Model: `gpt-4o-mini`
- API key: press Enter (already in `.env`)

---

## Generated Structure

```
financial_researcher/
└── src/
    └── financial_researcher/
        ├── config/
        │   ├── agents.yaml
        │   └── tasks.yaml
        ├── tools/          # Custom tools go here
        ├── crew.py
        └── main.py
```

---

## Key Takeaways (Preview)

- Tools in CrewAI are defined and assigned to agents similarly to OpenAI Agents SDK
- **Context** is an explicit YAML/code construct — you declare which task's output feeds into another task
- SerpDev provides free Google search capability — a practical alternative to OpenAI's hosted tool
- The same 5-step project setup applies to every new CrewAI project

---

## Up Next

Implementing tools and context in `agents.yaml`, `tasks.yaml`, and `crew.py` for the financial researcher crew.