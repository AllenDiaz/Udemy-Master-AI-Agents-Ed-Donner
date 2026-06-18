# Guardrails in OpenAI Agents SDK

## Overview

This lesson demonstrates **input and output guardrails** — safety mechanisms in the OpenAI Agents SDK that monitor agent inputs/outputs and can halt execution (trigger a "tripwire") when a condition is met. The example uses a guardrail to prevent personally identifiable information (PII) from being included in cold sales emails.

---

## What Are Guardrails?

Guardrails are protective layers attached to an agent that run checks on:

| Type | What It Checks |
|---|---|
| **Input guardrail** | The incoming user message before the agent processes it |
| **Output guardrail** | The agent's final response before it's returned |

When a guardrail detects a violation, it raises a **`GuardrailTripwireTriggered`** exception — immediately halting the workflow.

---

## Why Guardrails Matter (Real-World Use Case)

In a production sales automation tool:
- Users (e.g. a sales team) type prompts to kick off the email generation pipeline
- Guardrails ensure no **PII** (names, phone numbers, etc.) accidentally ends up in outbound cold emails
- They protect against misuse of the agentic system at the input boundary

> The guardrail isn't about catching obvious hardcoded values — it's about protecting against anything a user might type in at runtime.

---

## Implementation

### Attaching an Input Guardrail

```python
careful_sales_manager = Agent(
    name="Sales Manager",
    instructions=sales_manager_instructions,
    tools=tools,
    handoffs=[emailer_agent],
    model="gpt-4o-mini",
    input_guardrails=[guardrail_against_name]  # 👈 new
)
```

### How a Guardrail Works

A guardrail runs an LLM check (or custom logic) against the input. It returns a structured result:

```python
# Example guardrail output (Pydantic model)
class NameCheck(BaseModel):
    name: bool       # True if a real name was detected
    message: str     # Explanation
```

If `name == True` → tripwire is triggered → exception raised → workflow stops.

---

## Behavior in Action

### ❌ Tripwire Triggered

```python
# Input contains a real name → guardrail fires
result = await Runner.run(
    careful_sales_manager,
    "Send a cold sales email addressed to Dear CEO from Alice"
)
# Raises: GuardrailTripwireTriggered
# Guardrail: "guardrail_against_name" → name: True, message: "Alice"
```

### ✅ Passes Guardrail

```python
# No real name → guardrail passes → workflow runs normally
result = await Runner.run(
    careful_sales_manager,
    "Send a cold sales email addressed to the CEO from the Head of Business Development"
)
# Runs successfully → email generated and sent
```

---

## Key Takeaways

- Guardrails are attached at the **agent level** via `input_guardrails` or `output_guardrails`
- A triggered guardrail raises a **`GuardrailTripwireTriggered` exception** — handle it in your app
- Guardrails use **structured outputs (Pydantic)** to communicate what was detected
- They are most valuable in **production pipelines** where user input is unpredictable
- Both input and output guardrails can run on the same agent

---

## Week 2 Recap — What Was Covered

| Topic | Key Concept |
|---|---|
| OpenAI Agents SDK basics | `Agent`, `Runner`, `trace` |
| Async IO | `async`/`await`, event loop, `asyncio.gather()` |
| Tools | Wrapping functions and agents as tools |
| Agents as Tools | `.as_tool()` — agent becomes a callable tool |
| Handoffs | One-way delegation of control to another agent |
| Guardrails | Input/output safety checks with tripwire exceptions |
| Structured Outputs | Pydantic models for typed LLM responses |

---

## Exercises to Explore

- Try different models (Gemini, DeepSeek, Grok, Llama 3.3)
- Add more input and output guardrails (e.g. block phone numbers, block outdated copyright years)
- Replace plain text email output with a structured Pydantic object
- Add a Gradio UI to turn this into a usable sales automation tool

---

## Up Next

**Building Deep Research** — a multi-agent deep research system from scratch.