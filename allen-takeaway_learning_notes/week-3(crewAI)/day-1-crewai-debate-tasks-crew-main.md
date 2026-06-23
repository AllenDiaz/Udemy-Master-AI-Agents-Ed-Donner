# CrewAI — Tasks, crew.py, and main.py (Debate Crew Completion)

## Overview

This lesson completes the debate crew by defining **tasks in YAML**, assembling the crew in **`crew.py`**, and configuring runtime inputs in **`main.py`**. The full crew is then executed end-to-end.

---

## Defining Tasks — `tasks.yaml`

Three tasks for the debate crew:

```yaml
propose:
  description: >
    You are proposing the motion: {motion}.
    Come up with a clear argument in favor of the motion. Be very convincing.
  expected_output: >
    Your clear argument in favor of the motion in a concise manner.
  agent: debater
  output_file: outputs/propose.md

oppose:
  description: >
    You are in opposition to the motion: {motion}.
    Come up with a clear argument against the motion. Be very convincing.
  expected_output: >
    Your clear argument against the motion in a concise manner.
  agent: debater
  output_file: outputs/oppose.md

decide:
  description: >
    Review the arguments presented by the debaters and decide which side is more convincing.
  expected_output: >
    Your decision on which side is more convincing and why.
  agent: judge
  output_file: outputs/decide.md
```

**Key notes:**
- `{motion}` is the same template variable from `agents.yaml` — filled at runtime
- Both `propose` and `oppose` use the **same debater agent** — tasks differentiate the role
- Task names must not conflict with agent names (e.g. can't name a task `judge`)
- `output_file` saves each task's result to a markdown file automatically

---

## Assembling the Crew — `crew.py`

```python
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew

@CrewBase
class DebateCrew:
    agents_config = "config/agents.yaml"
    tasks_config  = "config/tasks.yaml"

    @agent
    def debater(self) -> Agent:
        return Agent(config=self.agents_config["debater"], verbose=True)

    @agent
    def judge(self) -> Agent:
        return Agent(config=self.agents_config["judge"], verbose=True)

    @task
    def propose(self) -> Task:
        return Task(config=self.tasks_config["propose"])

    @task
    def oppose(self) -> Task:
        return Task(config=self.tasks_config["oppose"])

    @task
    def decide(self) -> Task:
        return Task(config=self.tasks_config["decide"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,   # auto-populated by @agent decorators
            tasks=self.tasks,     # auto-populated by @task decorators
            process=Process.sequential,
            verbose=True
        )
```

> `self.agents` and `self.tasks` are automatically populated — no manual list management needed.

---

## Setting Inputs and Running — `main.py`

```python
from debate.crew import DebateCrew

inputs = {
    "motion": "There needs to be strict laws to regulate LLMs"
}

result = DebateCrew().crew().kickoff(inputs=inputs)
print(result.raw)
```

- `inputs` dict maps to template variables (`{motion}`) used across both YAML files
- `result.raw` prints the raw output from the **final task** (the judge's decision)

### Running the Crew

```bash
cd week3/crew/debate
crewai run
```

---

## Mixed-Model Crew (Bonus)

Assign different LLMs to different agents for interesting dynamics:

```yaml
# agents.yaml
debater:
  llm: openai/gpt-4o-mini   # OpenAI argues both sides

judge:
  llm: anthropic/claude-3-7-sonnet-latest  # Anthropic judges
```

> Result: Anthropic judging OpenAI's debate — and ruling in favor of strict LLM regulation.

---

## Output Files

After running, an `outputs/` directory is created with:

```
outputs/
├── propose.md    # Argument for the motion
├── oppose.md     # Argument against the motion
└── decide.md     # Judge's decision and reasoning
```

---

## Full Debate Crew Flow

```
main.py (kickoff with motion input)
    │
    ▼
[Task: propose] → debater agent → outputs/propose.md
    │
    ▼
[Task: oppose]  → debater agent → outputs/oppose.md
    │
    ▼
[Task: decide]  → judge agent   → outputs/decide.md + printed to terminal
```

---

## Key Takeaways

- `tasks.yaml` defines what each task does, what output is expected, which agent runs it, and where to save the result
- One agent can serve multiple tasks — tasks provide the role context, not the agent definition
- Template variables in YAML are resolved at `kickoff()` time via the `inputs` dict
- `crew.py` is intentionally minimal when YAML config does the heavy lifting
- `Process.sequential` runs tasks in the defined order — top to bottom in `tasks.yaml`
- Mixed-model crews are trivially configured via per-agent `llm` in YAML

---

## Related Concepts

- `Process.hierarchical` — manager LLM dynamically assigns tasks
- CrewAI `output_file` for persisting task results
- LiteLLM provider/model string format
- Template variables across agents and tasks YAML