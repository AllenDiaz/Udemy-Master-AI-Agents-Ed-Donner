# Week 5 Project — Agent Loop Live Run & Results

## Overview

This lesson captures the live run of the Agent Loop project — 5 framework agents collaborating in parallel under an ADK orchestrator to build a Spanish language-learning arcade website.

---

## Running the Project

```bash
cd week5/5_agent_loop
uv run agent_loop.py
```

Options:
```bash
uv run agent_loop.py --language French    # different language
uv run agent_loop.py --skip mastra        # skip a framework
```

---

## What Happened During the Run

### Phase 1 — Goal Assignment (~1 min)
- ADK orchestrator (Gemini 2.5 Flash) starts up
- Assigns 5 different game-building goals to the shared to-do board
- Each goal goes to a different framework worker

### Phase 2 — Parallel Building (~3-4 min)
All 5 workers ran **simultaneously**:

| Framework | Game Built |
|---|---|
| Strands | Color match game (harder as you level up) |
| Pydantic AI | Number guessing game |
| MAF | Greeting people in town game |
| Agno | Tapas ordering match game |
| Mastra | Verb action arcade (moving images) |

Each worker:
1. Read its goal from the shared board
2. Planned sub-steps autonomously
3. Built the game as vanilla HTML
4. Crossed off steps as completed

### Phase 3 — QA Testing (~1-2 min)
- ADK QA agent launched a Playwright browser
- Navigated to each game page
- Tested functionality via Playwright MCP server
- Reported pass/fail per game

### Phase 4 — CSS & Final Assembly
- CSS agent generated shared styling applied across all pages
- Orchestrator verified everything complete
- Final website launched locally ✅

---

## The Final Product

A fully functional Spanish language arcade with 5 unique mini-games — each with progressive difficulty. Built entirely by AI agents with no human code written.

> The point isn't that LLMs can build websites (you know that). The point is **how** it was done — agents in loops, guided only by a shared to-do list, achieving a coordinated goal.

---

## What Made It Work

```
SQLite to-do board (the only coordination mechanism)
        +
LLM token prediction consistent with tool use
        +
Focused, single-task agents
        =
Emergent collaborative behavior
```

No A2A. No complex messaging. Just tools and prompts.

---

## Reliability Notes

- MCP server timed out occasionally during QA testing — agent recovered and continued
- Smaller models may struggle — recommend `gpt-4o-mini` or better for workers
- Not deterministic — different game types and layouts each run
- May need a re-run if something goes significantly wrong

---

## Week 5 Final Challenge

> **Apply this framework to a problem that matters to you.**

Guidelines:
1. Keep the orchestrator + worker architecture
2. Pick 2–5 frameworks (don't need all 5)
3. Choose a domain: business problem, personal project, learning tool
4. Specialize each agent for a different sub-task
5. **Add a measurable outcome** — not just "LLM as judge" but a quantifiable score
6. Create a feedback loop: keep iterating until the score threshold is met

> A measurable outcome + feedback loop = significantly better results. This is the real power of agent loops.

Share your project: PR to community contributions → post on LinkedIn and tag the instructor.

---

## Week 5 Complete — Key Takeaways

| Lesson | Summary |
|---|---|
| All 6 frameworks | Same 5 steps, different syntax — pick what fits your team |
| Agent loop | LLM + tools + to-do list = emergent agentic behavior |
| Nested loops | Outer orchestrator + inner worker loops = sophisticated coordination |
| No A2A needed | Direct calls and prompts handle agent collaboration when you own all the code |
| Measurable outcomes | Quantifiable goals + feedback loops = better results |

---

## Up Next

**Week 6 — MCP (Model Context Protocol)**: the protocol that's been sprinkled throughout the course — now the full deep dive. 17% left to go.