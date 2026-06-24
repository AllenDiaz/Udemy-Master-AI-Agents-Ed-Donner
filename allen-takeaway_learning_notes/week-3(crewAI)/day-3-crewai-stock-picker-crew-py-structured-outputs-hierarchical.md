# CrewAI — Stock Picker `crew.py` (Structured Outputs, Custom Tools & Hierarchical Process)

## Overview

This lesson implements the stock picker crew in `crew.py`, introducing three new CrewAI concepts: **structured outputs via Pydantic**, **`output_pydantic` on tasks**, and the **hierarchical process** with a dedicated manager agent.

---

## Structured Outputs — Pydantic Schemas

Define schemas to constrain what agents must return. These act as guardrails on task output.

```python
from pydantic import BaseModel, Field

class TrendingCompany(BaseModel):
    """A company in the news attracting attention"""
    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Why this company is trending")

class TrendingCompanyList(BaseModel):
    companies: list[TrendingCompany]

class TrendingCompanyResearch(BaseModel):
    """Detailed research on a company"""
    name: str
    market_position: str
    future_outlook: str
    investment_potential: str

class TrendingCompanyResearchList(BaseModel):
    companies: list[TrendingCompanyResearch]
```

> 💡 Field descriptions are passed to the LLM — they guide the agent to populate each field meaningfully. Use consistent, clear terminology across all schemas, agents, and tasks.

---

## `crew.py` — Agents

```python
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool

@CrewBase
class StockPickerCrew:
    agents_config = "config/agents.yaml"
    tasks_config  = "config/tasks.yaml"

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(
            config=self.agents_config["trending_company_finder"],
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_researcher"],
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config=self.agents_config["stock_picker"],
            verbose=True
            # No search tool needed — works from context
        )
```

---

## `crew.py` — Tasks with `output_pydantic`

```python
    @task
    def find_trending_companies_task(self) -> Task:
        return Task(
            config=self.tasks_config["find_trending_companies_task"],
            output_pydantic=TrendingCompanyList   # ← structured output
        )

    @task
    def research_trending_companies_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_trending_companies_task"],
            output_pydantic=TrendingCompanyResearchList   # ← structured output
        )

    @task
    def pick_best_company_task(self) -> Task:
        return Task(config=self.tasks_config["pick_best_company_task"])
```

> `output_pydantic` forces the task to produce JSON conforming to the specified schema. This is how CrewAI implements structured outputs — equivalent to `output_type` in OpenAI Agents SDK.

---

## `crew.py` — Hierarchical Crew with Manager Agent

```python
    @crew
    def crew(self) -> Crew:
        manager = Agent(
            config=self.agents_config["manager"],
            allow_delegation=True   # required for hierarchical process
        )

        return Crew(
            agents=self.agents,       # the 3 worker agents (from @agent decorators)
            tasks=self.tasks,
            process=Process.hierarchical,   # ← manager decides task assignment
            manager_agent=manager,          # ← dedicated manager LLM
            verbose=True
        )
```

---

## Sequential vs. Hierarchical Process

| | `Process.sequential` | `Process.hierarchical` |
|---|---|---|
| **Task order** | Fixed — runs top to bottom | Dynamic — manager decides |
| **Manager needed** | No | Yes (`manager_agent` or `manager_llm`) |
| **Autonomy** | Low | High |
| **Reliability** | More predictable | More adventurous |
| **Use case** | Well-defined pipelines | Exploratory, autonomous workflows |

---

## Manager Agent Notes

- Defined **separately** from worker agents — not added to `self.agents`
- `allow_delegation=True` is required for the manager to assign tasks
- Use a **stronger model** (e.g. `gpt-4o` vs `gpt-4o-mini`) for the manager — it stays more coherent
- Alternative: `manager_llm="gpt-4o"` (skip defining a full agent), but a full agent with a defined role performs better

```python
# Alternative (simpler, slightly less reliable)
return Crew(
    ...,
    process=Process.hierarchical,
    manager_llm="gpt-4o"
)
```

---

## Key Takeaways

- `output_pydantic` on a task constrains its output to a Pydantic schema — same concept as `output_type` in OpenAI Agents SDK
- Field descriptions in Pydantic models actively guide LLM behavior — write them carefully
- The manager agent sits outside `self.agents` — it orchestrates, not executes
- Hierarchical process is more autonomous but less predictable — expect "adventures"
- Use a stronger model for the manager to maintain coherence in complex workflows
- Consistent terminology across YAML + Pydantic schemas = more stable outputs

---

## Related Concepts

- `Process.sequential` vs `Process.hierarchical`
- `allow_delegation=True` — equivalent to handoffs in OpenAI Agents SDK
- Pydantic `BaseModel` with `Field(description=...)` for schema documentation
- `output_pydantic` vs `output_file` — structured data vs. saved file