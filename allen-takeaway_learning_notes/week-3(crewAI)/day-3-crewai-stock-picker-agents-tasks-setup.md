# CrewAI — Stock Picker Crew (Agents, Tasks & Hierarchical Process)

## Overview

Day 3 of Week 3 builds the **stock picker crew** — a project that finds trending companies in a sector, researches them, and picks the best one for investment. It introduces three new concepts: **structured outputs in CrewAI**, **custom tools**, and the **hierarchical process**.

> ⚠️ This project is for learning purposes only — do not use its output for real trading decisions.

---

## Three New Concepts This Lesson

| Concept | Description |
|---|---|
| **Structured Outputs** | Returning typed Pydantic objects from CrewAI tasks |
| **Custom Tool** | Building your own tool (vs. using built-in ones like `SerperDevTool`) |
| **Hierarchical Process** | A manager LLM dynamically assigns tasks to agents |

---

## Scaffolding

```bash
cd week3/crew
crewai create crew stock_picker
```

---

## Agents — `agents.yaml`

Four agents for this crew:

```yaml
trending_company_finder:
  role: Trending Company Finder
  goal: Read the news, find 2-3 trending companies in {sector} for further analysis
  backstory: >
    You scan financial news to surface the hottest companies in a given sector.
  llm: openai/gpt-4o-mini

financial_researcher:
  role: Financial Researcher
  goal: Given trending companies, provide comprehensive analysis of each
  backstory: >
    A financial expert with a proven track record of deeply analyzing hot companies.
  llm: openai/gpt-4o-mini

stock_picker:
  role: Stock Picker
  goal: >
    Given researched companies with investment potential, select the best one,
    notify the user, and provide a detailed report. Don't pick the same company twice.
  backstory: >
    A meticulous, skilled financial analyst with a proven track record of equity selection.
  llm: openai/gpt-4o-mini

manager:
  role: Manager
  goal: Pick the best company for investment
  backstory: >
    A skilled project manager who can delegate tasks to achieve the goal.
  llm: openai/gpt-4o-mini
```

> The `manager` agent is used only in **hierarchical process** mode — it orchestrates which tasks get assigned to which agents dynamically.

---

## Tasks — `tasks.yaml`

```yaml
find_trending_companies_task:
  description: >
    Find the top trending companies in the news in {sector}.
    Search for new companies you haven't found before.
  expected_output: A list of trending companies in {sector}.
  agent: trending_company_finder
  output_file: outputs/trending_companies.json

research_trending_companies_task:
  description: >
    Given a list of trending companies, provide a detailed analysis
    of each company in a report.
  expected_output: A detailed research report on each trending company.
  agent: financial_researcher
  context:
    - find_trending_companies_task
  output_file: outputs/research.md

pick_best_company_task:
  description: >
    Analyze the research findings, pick the best company for investment,
    then send a push notification to the user.
    Provide a one-sentence rationale, then a detailed report on why you
    chose this company and which companies were not selected.
  expected_output: >
    A detailed investment recommendation report.
  agent: stock_picker
  context:
    - research_trending_companies_task
```

---

## Pro Tips from This Lesson

### 1. Consistent Language Across Agents and Tasks

Use the same terminology throughout your YAML files (e.g. "trending companies" appears in agent goals, task descriptions, and expected outputs). Inconsistent language causes less stable, less coherent outputs.

### 2. Context Chaining

```
find_trending_companies_task
    ↓ (context)
research_trending_companies_task
    ↓ (context)
pick_best_company_task
```

Each task builds on the previous one's output — context is the glue.

### 3. Output Files

- Use `.json` for structured data meant to be consumed by the next step
- Use `.md` for human-readable reports
- Not every task needs an `output_file` — only persist what's useful

---

## Key Takeaways

- Four agents, three tasks — one agent (`manager`) reserved for hierarchical mode
- Tasks chain via `context` — each stage feeds the next
- The `manager` agent enables **hierarchical process**: it decides task assignments at runtime
- Consistent, precise language in prompts = more stable crew behavior
- Custom tools and structured outputs are implemented in `crew.py` (covered next)

---

## Up Next

- Implementing **structured outputs** (Pydantic) for task results in CrewAI
- Building a **custom tool** (push notification)
- Running with **hierarchical process** and observing the manager in action