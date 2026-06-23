# CrewAI Core Concepts — Agents, Tasks, and Crews

## Overview

This lesson covers the three core building blocks of CrewAI: **Agent**, **Task**, and **Crew**. It also introduces YAML-based configuration and the `crew.py` module structure with CrewAI's decorators.

---

## The Three Core Concepts

### 1. Agent

The smallest autonomous unit — an LLM with a defined identity.

| Property | Description |
|---|---|
| `role` | What the agent does (e.g. "Senior Researcher") |
| `goal` | What the agent is trying to achieve |
| `backstory` | Context that shapes how the agent approaches its work |
| `tools` | Tools available to the agent |
| `memory` | Whether the agent retains memory across tasks |
| `llm` | The underlying language model |

> Compare to OpenAI Agents SDK: agents there just had `instructions` (a free-form system prompt). CrewAI is more **prescriptive** — role/goal/backstory are separate fields that get composed into a system prompt behind the scenes.

**Trade-off:**

| | CrewAI | OpenAI Agents SDK |
|---|---|---|
| **Structure** | Opinionated (role, goal, backstory) | Flexible (one `instructions` field) |
| **Best practice enforcement** | Built-in | Manual |
| **Debuggability** | Harder (system prompt is abstracted) | Easier (you wrote the system prompt) |

---

### 2. Task

A specific assignment given to an agent. **New concept — no direct analog in OpenAI Agents SDK.**

| Property | Description |
|---|---|
| `description` | What needs to be done |
| `expected_output` | What a successful result looks like |
| `agent` | The agent assigned to this task |

> One agent can have multiple tasks. Tasks make the work unit explicit and trackable.

---

### 3. Crew

A team of agents and tasks working together.

```
Crew = Agents + Tasks + Process Mode
```

**Two process modes:**

| Mode | Behavior |
|---|---|
| `sequential` | Tasks execute one by one in defined order |
| `hierarchical` | A manager LLM dynamically assigns tasks to agents |

---

## YAML Configuration

CrewAI encourages defining agents and tasks in **YAML files**, separating configuration from code.

### Example: `agents.yaml`

```yaml
researcher:
  role: Senior Researcher
  goal: Uncover cutting-edge developments in AI
  backstory: >
    You are a seasoned researcher with a passion for discovering
    the latest breakthroughs in artificial intelligence.
  llm: gpt-4o-mini
```

### Using Config in Code

```python
# Instead of hardcoding all fields...
researcher = Agent(
    config=self.agents_config["researcher"]  # pulls from YAML
)
```

**Benefits of YAML config:**
- Keeps prompts out of code — cleaner separation of concerns
- Easier to iterate on prompts without touching logic
- Works for both agents and tasks

---

## `crew.py` — Where Everything Comes Together

The central module that defines your agents, tasks, and crew using **decorators**.

```python
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew

@CrewBase
class MyResearchCrew:

    @agent
    def researcher(self) -> Agent:
        return Agent(config=self.agents_config["researcher"])

    @agent
    def writer(self) -> Agent:
        return Agent(config=self.agents_config["writer"])

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config["research_task"])

    @task
    def writing_task(self) -> Task:
        return Task(config=self.tasks_config["writing_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,     # auto-populated by @agent decorators
            tasks=self.tasks,       # auto-populated by @task decorators
            process=Process.sequential
        )
```

**Key decorators:**

| Decorator | Purpose |
|---|---|
| `@CrewBase` | Marks the class as a crew definition |
| `@agent` | Registers the function's return value into `self.agents` |
| `@task` | Registers the function's return value into `self.tasks` |
| `@crew` | Defines the function that assembles and returns the `Crew` |

> `self.agents` and `self.tasks` are automatically populated by the decorators — no manual list management needed.

---

## Key Takeaways

- **Agent** = LLM + role + goal + backstory + tools
- **Task** = assignment with description, expected output, and an assigned agent
- **Crew** = team of agents + tasks + process mode (sequential or hierarchical)
- YAML config cleanly separates prompts from logic
- `crew.py` with decorators is the standard way to define a CrewAI project
- CrewAI is more opinionated than OpenAI Agents SDK — a trade-off between structure and flexibility

---

## Related Concepts

- `Process.sequential` vs `Process.hierarchical`
- CrewAI YAML config for agents and tasks
- Python decorators (used heavily in CrewAI's design)
- OpenAI Agents SDK comparison: `instructions` vs `role/goal/backstory`