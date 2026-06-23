# First Look at OpenAI Agents SDK

## Overview

This lesson introduces the **OpenAI Agents SDK** (formerly Swarm), covering its three core building blocks: `Agent`, `Runner`, and `Trace`. It also reinforces why `async`/`await` is required when working with the SDK.

---

## Key Imports

```python
from dotenv import load_dotenv
from agents import Agent, Runner, trace

load_dotenv(override=True)
```

> The OpenAI agents package is simply called `agents`.

---

## Core Building Blocks

### 1. `Agent`

An `Agent` is an **LLM instance with a specific system prompt**, oriented around a single task.

```python
agent = Agent(
    name="Jokester",
    instructions="You are a joke teller.",  # This is the system prompt
    model="gpt-4o-mini"
)
```

**Key parameters:**

| Parameter | Description |
|---|---|
| `name` | Human-readable label for the agent |
| `instructions` | The system prompt — defines the agent's role/behavior |
| `model` | The LLM to use (defaults to OpenAI, but other models are supported) |

> The SDK is **not** locked to OpenAI models — other providers can be used.

**Agent object also exposes:**
- `handoffs` — for agent-to-agent interactions (covered later)
- `input_guardrails` / `output_guardrails` — safety controls (covered later)

---

### 2. `Runner`

Executes an agent with a given user message.

```python
# ❌ Wrong — Runner.run() is async, returns a coroutine object
result = Runner.run(agent, "Tell a joke about autonomous AI agents")

# ✅ Correct — must use await
result = await Runner.run(agent, "Tell a joke about autonomous AI agents")

print(result.final_output)
```

> `Runner.run()` is an **async method** — calling it without `await` returns a coroutine object, not the result. This is expected behavior from the previous async IO lesson.

---

### 3. `trace` (Context Manager)

Wraps agent interactions so they are **recorded and visible** in OpenAI's monitoring dashboard (`platform.openai.com → Traces`).

```python
with trace("Telling a Joke"):
    result = await Runner.run(agent, "Tell a joke about autonomous AI agents")
    print(result.final_output)
```

- Groups all LLM calls under a single labeled trace
- Invaluable for debugging complex multi-agent workflows
- Shows: system prompt, user message, assistant response, and more

---

## Async Behavior — Quick Reminder

`Runner.run()` is a **coroutine**, not a regular function:

```python
# Calling without await → returns coroutine object (nothing runs)
result = Runner.run(agent, "...")       # ❌ coroutine object

# Calling with await → executes and returns actual result
result = await Runner.run(agent, "...") # ✅ RunResult object
```

Access the response via `result.final_output`.

---

## Full Working Example

```python
from agents import Agent, Runner, trace
from dotenv import load_dotenv

load_dotenv(override=True)

agent = Agent(
    name="Jokester",
    instructions="You are a joke teller.",
    model="gpt-4o-mini"
)

with trace("Telling a Joke"):
    result = await Runner.run(agent, "Tell a joke about autonomous AI agents")
    print(result.final_output)
```

---

## Key Takeaways

- `Agent` = LLM + system prompt + model config
- `Runner.run()` = async execution engine — always use `await`
- `trace()` = observability wrapper for the OpenAI dashboard
- The SDK supports non-OpenAI models despite the name
- This lesson covers the basic construct — handoffs, guardrails, and multi-agent patterns come later

---

## Related Concepts to Explore

- `Agent` handoffs between multiple agents
- Input/output guardrails
- Using non-OpenAI models with the Agents SDK
- OpenAI Traces dashboard (`platform.openai.com/traces`)