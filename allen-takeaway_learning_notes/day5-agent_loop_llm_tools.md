# The Agent Loop — LLMs with Tools in a Loop to Achieve a Goal

## Overview

This lesson revisits and sharpens the definition of **AI agents**, then demonstrates — from first principles — how to build a simple but powerful **agent loop** using only the OpenAI library and plain Python.

---

## Evolving Definition of "Agent"

| Era | Definition |
|---|---|
| Early days (OpenAI/Altman) | AI systems that can do work for you independently |
| Early 2025 (Anthropic/HuggingFace consensus) | AI systems where an **LLM controls the workflow** |
| **2026 (current)** | An **LLM equipped with tools that runs those tools in a loop to achieve a goal** |

> 💡 **Key insight (Simon Willison):** "You know it when you see it" — an LLM looping through tool calls until a goal is satisfied.

---

## What's Actually Happening Under the Hood

Despite *feeling* like a smart autonomous agent working independently, the reality is:

- Your code **repeatedly calls an LLM** in a `while` loop
- The LLM returns **tokens** — some of which are tool call instructions
- Your code **interprets** those tokens, **executes the tool**, and feeds results back
- This continues until the LLM decides it's done (no more tool calls needed)

> The "thinking, planning agent" is an **illusion** — it's a while loop calling a token generator.

---

## Key Components Built in This Lesson

### 1. To-Do List (Plain Python State)

```python
todos = []
completed = []

def create_todos(descriptions: list[str]):
    # Adds tasks to todos, marks all as incomplete
    ...

def mark_completed(index: int, notes: str):
    # Strikes through completed task, prints updated list
    ...
```

- `todos` — list of task strings
- `completed` — list of booleans (`True`/`False`)

### 2. Tool Definitions (JSON Schema)

Two tools described in JSON for the LLM:

- **`create_todos`** — takes a list of task descriptions and adds them
- **`mark_completed`** — takes an index and completion notes

```python
tools = [create_todos_json, mark_completed_json]
```

### 3. `handle_tool_calls()` Function

- Iterates over tool calls returned by the LLM
- Uses Python's `globals()` trick to dynamically dispatch to the correct function
- Same pattern as used in prior lessons (reusable)

### 4. The Agent Loop

```python
def loop(messages):
    done = False
    while not done:
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=messages,
            tools=tools,
            reasoning_effort="none"  # keeps it fast
        )
        finish_reason = response.choices[0].finish_reason

        if finish_reason == "tool_calls":
            # Execute tools, append results to messages
            handle_tool_calls(response, messages)
        else:
            # LLM is satisfied — exit loop
            done = True
            show(response.choices[0].message.content)
```

---

## Practical Example

**User prompt:** *"A train leaves Boston at 2pm traveling 60mph. Another train leaves New York at 3pm traveling 80mph towards Boston. When do they meet?"*

**What the agent did autonomously:**
1. ✅ Created to-dos: Interpret problem → Set up variables → Estimate missing quantity → Compute
2. ✅ Worked through each step, crossing items off the list
3. ✅ Returned the final answer

> No human interaction. No framework. Just a while loop + tools.

---

## Key Takeaways

- Agentic behavior = **LLM + tools + loop** — nothing more
- This pattern produces **better outcomes** than single-shot prompting for complex problems
- Tools can be anything: file creation, calculations, API calls, search — the pattern scales
- Frameworks like Claude Code are built on this same fundamental loop
- Understanding internals > memorizing syntax

---

## Exercise Challenge

> Build your own agent loop **from scratch** in a fresh Python notebook.

Suggested steps:
1. Create a simple state (to-do list or similar)
2. Write 2–3 plain Python functions as tools
3. Define their JSON schemas
4. Write a `handle_tool_calls()` dispatcher
5. Write the `while not done` loop
6. Give it an interesting problem and watch it go
7. *(Bonus)* Add extra tools and observe improved behavior

---

## Related Concepts

- Tool use / function calling in OpenAI API
- Agentic design patterns (evaluator-optimizer, planner-executor)
- Rich console for formatted terminal output
- Reasoning models vs. standard completion models