# CrewAI — Financial Researcher Crew (Agents, Tasks, Context & Mixed Models)

## Overview

This lesson builds the **financial researcher crew** end-to-end — two agents (researcher + analyst), two tasks with **context passing**, and a mixed-model setup using DeepSeek and Groq/Llama.

---

## Agents — `agents.yaml`

```yaml
researcher:
  role: Senior Financial Researcher for {company}
  goal: Research {company}'s news, current status, and investment potential
  backstory: >
    You are a seasoned financial researcher with a talent for finding the most
    relevant information about a company. Known for presenting findings in a
    clear and concise manner.
  llm: deepseek/deepseek-chat

analyst:
  role: Market Analyst and Report Writer focused on {company}
  goal: >
    Analyze {company} and create a comprehensive, well-structured report that
    represents insights in a clear and engaging way.
  backstory: >
    You are a meticulous, skilled analyst with a background in financial analysis
    and company research, with a talent for crafting meaningful insights from data.
  llm: groq/llama-3.3-70b-versatile
```

> The `backstory` field encourages richer prompting — words like "meticulous" and "meaningful insights" condition the LLM toward higher quality outputs.

---

## Tasks — `tasks.yaml`

### Research Task

```yaml
research_task:
  description: >
    Conduct thorough research on {company}. Focus on:
    - Current status and financial health
    - Historical performance, challenges, and opportunities
    - Recent news and developments
    - Future outlook and potential
    Organize findings in a structured format with clear sections.
  expected_output: >
    Well-defined sections covering all key areas of {company}'s research.
  agent: researcher
```

### Analysis Task

```yaml
analysis_task:
  description: >
    Analyze the research findings and create a comprehensive report on {company}.
    Include: Executive Summary, Key Insights, Market Outlook.
    Format in a professional, polished style.
  expected_output: >
    A polished, professional report on {company} based on the research findings.
  agent: analyst
  context:
    - research_task       # ← passes research_task output as input to this task
  output_file: outputs/report.md
```

---

## Key Concept: `context`

The `context` field in a task definition **explicitly passes the output of one task as input to another**.

```yaml
analysis_task:
  context:
    - research_task   # analyst receives researcher's full output automatically
```

- Ensures continuity between tasks without manual wiring
- Works as a list — a task can receive context from multiple prior tasks
- Only the final task needs an `output_file` if intermediate results aren't needed separately

---

## `crew.py`

```python
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew

@CrewBase
class FinancialResearcherCrew:
    agents_config = "config/agents.yaml"
    tasks_config  = "config/tasks.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(config=self.agents_config["researcher"], verbose=True)

    @agent
    def analyst(self) -> Agent:
        return Agent(config=self.agents_config["analyst"], verbose=True)

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config["research_task"])

    @task
    def analysis_task(self) -> Task:
        return Task(config=self.tasks_config["analysis_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
```

---

## `main.py`

```python
from financial_researcher.crew import FinancialResearcherCrew

inputs = {"company": "Tesla"}

result = FinancialResearcherCrew().crew().kickoff(inputs=inputs)
print(result.raw)
```

Run with:
```bash
crewai run
```

---

## Mixed-Model Crew

Two different providers used in a single crew:

| Agent | Model | Provider |
|---|---|---|
| Researcher | `deepseek/deepseek-chat` | DeepSeek (671B) |
| Analyst | `groq/llama-3.3-70b-versatile` | Groq (Meta Llama 3.3) |

> DeepSeek is thorough but slow (~30s). Groq is extremely fast. This is a practical example of matching model choice to task requirements.

**Other valid options:**
```yaml
llm: openai/gpt-4o-mini         # Fast, cheap
llm: anthropic/claude-3-5-sonnet # High quality
llm: ollama/llama3.2             # Local, free
```

---

## Full Workflow

```
main.py → kickoff(inputs={"company": "Tesla"})
    │
    ▼
[research_task] → researcher (DeepSeek) → finds and structures company data
    │
    ▼  (output passed via context)
[analysis_task] → analyst (Groq/Llama) → synthesizes report → outputs/report.md
```

---

## Key Takeaways

- `context` in `tasks.yaml` is the clean CrewAI way to pass data between tasks
- The `backstory` field actively improves output quality — use descriptive, intentional language
- Per-agent `llm` in YAML makes mixed-model crews trivially easy to configure
- Match model to task: use fast models (Groq) for synthesis, powerful models (DeepSeek) for research
- Only the final consumer task needs `output_file` — intermediate results flow via `context`

---

## Up Next

Adding **tools** (SerpDev Google search) to the financial researcher crew.