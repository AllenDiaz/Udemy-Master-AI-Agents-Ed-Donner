# CrewAI — LiteLLM Integration and Project Setup

## Overview

This lesson covers two topics: how CrewAI connects to LLMs via **LiteLLM**, and how to scaffold a new CrewAI project using the CLI.

---

## LiteLLM — Flexible LLM Integration

CrewAI uses **LiteLLM** under the hood to communicate with any LLM provider. It's an extremely lightweight abstraction — almost the opposite of LangChain in terms of overhead.

### Model Name Convention

```
provider/model-name
```

### Supported Providers

```python
from crewai import LLM

llm = LLM(model="openai/gpt-4o-mini")        # OpenAI
llm = LLM(model="anthropic/claude-3-5-sonnet") # Anthropic
llm = LLM(model="gemini/gemini-flash")         # Google Gemini
llm = LLM(model="groq/llama-3.3-70b")         # Groq (Llama)
llm = LLM(model="xai/grok-2")                 # xAI Grok
llm = LLM(model="ollama/llama3", base_url="http://localhost:11434")  # Local via Ollama
llm = LLM(model="openrouter/openai/gpt-4o")   # OpenRouter (multi-provider abstraction)
```

> CrewAI's LiteLLM integration is a clear **advantage over OpenAI Agents SDK** — switching models across providers is trivial.

---

## CrewAI Project Structure

CrewAI projects are scaffolded via CLI, not just notebooks. Each crew gets its own directory structure.

### Create a New Project

```bash
# Create a crew project
crewai create crew my_crew

# (Alternative) Create a flow project
crewai create flow my_project
```

### Generated Directory Structure

```
my_crew/
└── src/
    └── my_crew/
        ├── config/
        │   ├── agents.yaml      # Agent definitions (role, goal, backstory, llm)
        │   └── tasks.yaml       # Task definitions (description, expected_output)
        ├── crew.py              # Crew assembly with decorators
        └── main.py              # Entry point — kicks off the crew run
```

### Running the Crew

```bash
crewai run
# equivalent to: uv run main.py
```

---

## Key Files at a Glance

| File | Purpose |
|---|---|
| `config/agents.yaml` | Define agent roles, goals, backstories, and LLMs |
| `config/tasks.yaml` | Define task descriptions and expected outputs |
| `crew.py` | Assemble agents, tasks, and crew using decorators |
| `main.py` | Entry point — instantiate and run the crew |

---

## Project Tooling Note

CrewAI uses **`uv`** for project/dependency management — same as the rest of the course. Running `crewai create crew` scaffolds a `uv` project inside your existing `uv` workspace.

> You'll have nested `uv` projects: one for the whole course, and one per CrewAI crew inside it. This will make more sense when seen in action.

---

## Key Takeaways

- LiteLLM makes CrewAI provider-agnostic — switch models with a one-line change
- Model naming format: `provider/model-name`
- CrewAI requires real Python modules — not just notebooks
- `crewai create crew` scaffolds the full project structure automatically
- The `config/` YAML files keep prompts cleanly separated from code
- `crew.py` is the heart of the project; `main.py` is the runner

---

## Related Concepts

- LiteLLM documentation
- `uv` project management
- `crew.py` decorators (`@CrewBase`, `@agent`, `@task`, `@crew`)
- CrewAI Flows vs. Crews