# CrewAI — Coder Agent (Code Execution with Docker)

## Overview

This lesson builds a **coder agent** — a CrewAI agent that can write Python code, execute it in a Docker sandbox, interpret the results, and iterate. This pattern is commonly called a **code agent**.

---

## What Is a Code Agent?

A code agent doesn't just *generate* code — it:
1. Plans how to solve the problem with code
2. Writes the Python code
3. **Executes** the code and reads the output
4. Interprets results and takes further action if needed

> Code execution is a **means to an end** — the agent uses code as a tool for problem solving, not just as a deliverable.

---

## Docker — Safe Code Execution

When `code_execution_mode="safe"`, CrewAI runs generated code inside a **Docker container** — an isolated sandbox that cannot damage the host system.

**Install Docker:** [docker.com/get-started](https://www.docker.com/get-started) — one-click install for Mac, Windows, Linux.

> If Docker is not running, code execution falls back to running directly on your machine.

---

## Project Setup

```bash
crewai create crew coder
```

---

## `agents.yaml`

```yaml
coder:
  role: Python Developer
  goal: >
    Write Python code to achieve this assignment: {assignment}.
    First plan how the code will work, then write it, then run it and check the output.
  backstory: >
    A seasoned Python developer with a knack for writing clean, efficient code.
  llm: openai/gpt-4o-mini
```

---

## `tasks.yaml`

```yaml
coding_task:
  description: >
    Write Python code to achieve this assignment: {assignment}.
  expected_output: >
    A text file that includes the code and the output of running the code.
  agent: coder
  output_file: outputs/code_and_output.txt
```

> Requesting both the **code and the output** in the expected output ensures you can verify what the agent actually ran.

---

## `crew.py`

```python
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew

@CrewBase
class CoderCrew:
    agents_config = "config/agents.yaml"
    tasks_config  = "config/tasks.yaml"

    @agent
    def coder(self) -> Agent:
        return Agent(
            config=self.agents_config["coder"],
            verbose=True,
            allow_code_execution=True,        # ← enables code writing + running
            code_execution_mode="safe",       # ← runs in Docker container
            max_execution_time=30,            # ← 30 second timeout per execution
            max_retry_limit=5                 # ← up to 5 retry attempts
        )

    @task
    def coding_task(self) -> Task:
        return Task(config=self.tasks_config["coding_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
```

**Key parameters on the agent:**

| Parameter | Purpose |
|---|---|
| `allow_code_execution=True` | Enables the agent to write and run code |
| `code_execution_mode="safe"` | Runs code in a Docker container (sandboxed) |
| `max_execution_time=30` | Kills execution if it runs longer than 30 seconds |
| `max_retry_limit=5` | Agent can retry up to 5 times if code fails |

---

## `main.py`

```python
from coder.crew import CoderCrew

inputs = {
    "assignment": "Write a script that calculates the first 20 Fibonacci numbers and prints them."
}

result = CoderCrew().crew().kickoff(inputs=inputs)
print(result.raw)
```

Run with:
```bash
crewai run
```

---

## Key Takeaways

- `allow_code_execution=True` is the only required change to give an agent code execution ability
- `code_execution_mode="safe"` uses Docker for sandboxed, safe execution — highly recommended
- The agent autonomously plans → writes → runs → interprets — no manual orchestration needed
- Requesting both code and output in `expected_output` lets you verify the agent's work
- This is one of the most powerful features of CrewAI — trivial to enable, significant in capability
- Docker must be installed and running for safe mode to work

---

## Related Concepts

- Docker containers and sandboxing
- Code agents / "Coda agents" in the broader AI ecosystem
- `max_retry_limit` — agent self-correction loop
- CrewAI `output_file` for persisting results