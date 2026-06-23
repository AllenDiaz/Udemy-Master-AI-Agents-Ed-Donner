# CrewAI — Building the Debate Crew (Project Setup & Agent YAML)

## Overview

This lesson walks through scaffolding a real CrewAI project from scratch — a **debate crew** with two agents (a debater and a judge) — and defining them via `agents.yaml`.

---

## Scaffolding the Project

```bash
# Navigate to the week 3 folder
cd week3/crew

# Create the crew project
crewai create crew debate
```

During setup, CLI prompts:
- **Model provider** → `openai`
- **Model** → `gpt-4o-mini`
- **API key** → press Enter (already in `.env`)

---

## Generated Project Structure

```
debate/
├── knowledge/
│   └── user_preference.txt     # Optional user context (not used here)
└── src/
    └── debate/
        ├── config/
        │   ├── agents.yaml     # Agent definitions
        │   └── tasks.yaml      # Task definitions
        ├── tools/              # Custom tool scaffolding (unused here)
        ├── crew.py             # Crew assembly with decorators
        └── main.py             # Entry point — sets inputs and runs crew
```

> The most important directory is `src/debate/` — this is where all your actual crew logic lives.

---

## Defining Agents — `agents.yaml`

Two agents for the debate crew:

### 1. Debater Agent

Plays **both for and against** roles — tasks distinguish which side it argues.

```yaml
debater:
  role: A compelling debater
  goal: >
    Present a clear argument either in favor of or against the motion: {motion}
  backstory: >
    You are an experienced debater with a knack for giving concise but
    convincing arguments. The motion is: {motion}
  llm: gpt-4o-mini
```

### 2. Judge Agent

Evaluates both arguments and picks a winner.

```yaml
judge:
  role: Decide the winner of the debate based on the arguments presented
  goal: >
    Evaluate both sides of the debate and declare a winner based purely
    on the strength of the arguments.
  backstory: >
    You are a fair judge with a reputation for weighing up arguments without
    factoring in your own views, making a decision based purely on the merits
    of the argument. The motion is: {motion}
  llm: gpt-4o-mini
```

---

## Key YAML Concepts

### Template Variables

Curly braces `{motion}` act as **template placeholders** — filled at runtime from `main.py`.

```yaml
goal: Present a clear argument for or against: {motion}
```

At runtime in `main.py`:
```python
crew.kickoff(inputs={"motion": "AI will replace software engineers by 2030"})
```

### Specifying the LLM

```yaml
# Short form (assumes OpenAI by default)
llm: gpt-4o-mini

# Explicit form
llm: openai/gpt-4o-mini
```

---

## Agent Design Notes

- **Role** → what the agent *is* (a job title / identity)
- **Goal** → what the agent is *trying to achieve* (objective)
- **Backstory** → context that shapes behavior (key part of the system prompt)

> Scientifically: the backstory conditions the LLM's token predictions. Input tokens matching a context make the model more likely to generate output consistent with that context.

- One `debater` agent handles both "for" and "against" sides — **tasks** differentiate the roles, not separate agents
- Including `{motion}` in both `goal` and `backstory` ensures the agent stays on topic

---

## Key Takeaways

- `crewai create crew <name>` scaffolds the full project in one command
- `agents.yaml` cleanly separates agent definitions from Python code
- Template variables (`{motion}`) make agents reusable across different inputs
- `llm` can be set per-agent in YAML — enabling mixed-model crews
- The same agent can serve multiple roles when tasks define the specific behavior

---

## Up Next

Defining **tasks** in `tasks.yaml` and assembling the crew in `crew.py`.