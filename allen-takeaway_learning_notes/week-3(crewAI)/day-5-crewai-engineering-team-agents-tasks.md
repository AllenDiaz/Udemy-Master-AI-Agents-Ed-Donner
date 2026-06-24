# CrewAI — Engineering Team Crew (Agents & Tasks)

## Overview

The final CrewAI project of Week 3 extends the coder agent into a full **engineering team crew** — an engineering lead, backend engineer, frontend engineer, and test engineer working together to design, build, demo, and test a Python module end-to-end.

---

## Project Setup

```bash
crewai create crew engineering_team
```

---

## The Team

```
Engineering Lead      → designs the module
Backend Engineer      → writes the Python code
Frontend Engineer     → builds a Gradio UI demo
Test Engineer         → writes unit tests
```

---

## Agents — `agents.yaml`

### Engineering Lead
```yaml
engineering_lead:
  role: Engineering Lead for the engineering team
  goal: >
    Take the high level requirements and prepare a detailed design for the backend developer.
    Everything should be in one Python module — completely self-contained and testable.
    Describe function/method signatures. Requirements: {requirements}.
    Module name: {module_name}. Class name: {class_name}.
  backstory: A seasoned engineering lead with a knack for writing clear and concise designs.
  llm: openai/gpt-4o
```

### Backend Engineer
```yaml
backend_engineer:
  role: Python Engineer
  goal: >
    Write a Python module that implements the design described by the engineering lead.
    Requirements: {requirements}. Module: {module_name}. Class: {class_name}.
  backstory: >
    A Python engineer with a knack for writing clean, efficient code.
    Follow the design instructions carefully.
  llm: anthropic/claude-3-7-sonnet-latest
```

### Frontend Engineer
```yaml
frontend_engineer:
  role: Gradio Expert
  goal: >
    Write a simple Gradio UI that demonstrates the given backend.
    All in one file (app.py) in the same directory as the backend module.
    Keep the UI simple and clean. Requirements: {requirements}.
  backstory: A seasoned engineer highly skilled at writing simple Gradio UIs for a backend class.
  llm: anthropic/claude-3-7-sonnet-latest
```

### Test Engineer
```yaml
test_engineer:
  role: QA Engineer and Python Developer
  goal: >
    Write unit tests for the given backend module.
    Create a test file named test_{module_name}.py in the same directory.
  backstory: A seasoned QA engineer who writes great unit tests for Python code.
  llm: deepseek/deepseek-chat
```

**Mixed model strategy:**

| Agent | Model | Reason |
|---|---|---|
| Engineering Lead | `gpt-4o` | Stronger model for architecture decisions |
| Backend Engineer | `claude-3-7-sonnet` | Excellent coding model |
| Frontend Engineer | `claude-3-7-sonnet` | Consistent with backend context |
| Test Engineer | `deepseek-chat` | Strong at code analysis and testing |

---

## Tasks — `tasks.yaml`

### Design Task
```yaml
design_task:
  description: >
    Take the high level requirements and prepare a detailed design for the engineer.
  expected_output: >
    A detailed design for the engineer in markdown format only.
    Do NOT write any code — output the design only.
  agent: engineering_lead
  output_file: outputs/{module_name}_design.md
```

### Code Task
```yaml
code_task:
  description: >
    Write a Python module that implements the design as described by the engineering lead
    to achieve the requirements.
    IMPORTANT: Output only raw Python code — no markdown formatting, no code block
    delimiters, no backticks.
  expected_output: Raw Python code only.
  agent: backend_engineer
  context:
    - design_task
  output_file: outputs/{module_name}.py
```

### Frontend Task
```yaml
frontend_task:
  description: >
    Write a Gradio UI in app.py that demonstrates the given backend class.
    Assume one user. Keep the UI simple and clean.
    Requirements: {requirements}.
    IMPORTANT: Output only raw Python code — no markdown, no backticks.
  expected_output: Raw Python code only.
  agent: frontend_engineer
  context:
    - code_task
  output_file: outputs/app.py
```

### Test Task
```yaml
test_task:
  description: >
    Write unit tests for the given backend module.
    Create test_{module_name}.py in the same directory.
    IMPORTANT: Output only raw Python code — no markdown, no backticks.
  expected_output: Raw Python code only.
  agent: test_engineer
  context:
    - code_task
  output_file: outputs/test_{module_name}.py
```

---

## Key Design Decisions

### 1. Suppress Markdown in Code Output
LLMs default to wrapping code in markdown fences (` ```python `). Always add this to coding tasks:

```
IMPORTANT: Output only the raw Python code without any markdown formatting,
code block delimiters, or backticks.
```

### 2. Template Variables in Output File Names
```yaml
output_file: outputs/{module_name}_design.md   # resolved at runtime
output_file: outputs/test_{module_name}.py
```

### 3. Context Chaining

```
design_task
    ↓ (context)
code_task
    ↓ (context)        ↓ (context)
frontend_task       test_task
```

Frontend and test tasks both receive the backend code as context — independently but simultaneously.

### 4. Agents as System Prompts / Tasks as User Prompts
> Agents define the **system prompt** (who the agent is).  
> Tasks define the **user prompt** (what it needs to do right now).  
> `context` injects prior task outputs into that user prompt.

---

## Key Takeaways

- A real engineering workflow is modeled cleanly with 4 agents and 4 tasks
- Mixed models across agents lets you optimize for quality, speed, and cost per role
- Suppressing markdown in code outputs is essential — always include the explicit instruction
- Template variables work everywhere in YAML — descriptions, goals, and output file names
- `context` creates a dependency graph — frontend and test tasks branch off code_task in parallel

---

## Up Next

Implementing `crew.py` and `main.py` and running the full engineering team end-to-end.