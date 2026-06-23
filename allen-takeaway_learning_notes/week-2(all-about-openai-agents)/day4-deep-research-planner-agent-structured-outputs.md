# Deep Research — Planner Agent and Structured Outputs

## Overview

This lesson builds the **planner agent** — the component responsible for taking a research query and generating a structured list of web searches to run. It makes heavy use of **structured outputs** with Pydantic, and introduces two important techniques: field annotations and chain-of-thought via a `reason` field.

---

## The Planner Agent's Role

```
User Query
    │
    ▼
Planner Agent  →  outputs a WebSearchPlan (list of searches)
    │
    ▼
Search Agent   →  executes each search (covered in previous lesson)
```

The planner doesn't search — it **plans what to search**.

---

## Structured Outputs with Pydantic

### Why Structured Outputs?

Instead of returning natural language text, the agent returns a **typed Python object** (backed by JSON under the hood). This makes the output reliable, parseable, and easy to use programmatically.

> When you hear "the model returns an object" — it's generating JSON that the client library deserializes into a Pydantic model. No magic.

---

### Schema Definition

#### `WebSearchItem` — A single search

```python
from pydantic import BaseModel

class WebSearchItem(BaseModel):
    reason: str
    """Why this search is important for answering the query"""

    query: str
    """The actual search term to use"""
```

> 💡 **Tip:** Docstrings on fields are passed to the model as context. They tell the model *why* it's populating each field, leading to better outputs.

#### `WebSearchPlan` — The full plan

```python
class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    """A list of web searches to perform to best answer the query"""
```

---

## The `reason` Field — Chain-of-Thought Effect

Asking the model to output a `reason` **before** the `query` creates a chain-of-thought effect:

- The model first predicts tokens describing *why* a search is needed
- When it then predicts the query tokens, they are more consistent with that rationale
- Result: higher quality, more coherent search queries

> This is not magic — it's a side effect of next-token prediction. Predicting a reason first conditions the model toward a better query prediction.

This is equivalent to **chain-of-thought prompting** built directly into the output schema.

---

## Planner Agent Implementation

```python
planner_agent = Agent(
    name="Planner Agent",
    instructions="""
        You are a helpful research assistant.
        Given a query, come up with a set of web searches to perform
        to best answer that query. Output exactly 3 search terms.
    """,
    model="gpt-4o-mini",
    output_type=WebSearchPlan   # 👈 structured output
)
```

**Key parameter:** `output_type=WebSearchPlan` — tells the agent to return a `WebSearchPlan` object instead of plain text.

---

## Running the Planner

```python
result = await Runner.run(planner_agent, "Latest AI agent frameworks in 2025")
plan = result.final_output  # WebSearchPlan object

for item in plan.searches:
    print(item.reason)
    print(item.query)
```

**Example output:**

| Reason | Query |
|---|---|
| Find the most recent developments in AI agent frameworks for 2025 | latest AI agent frameworks 2025 |
| Explore industry-specific or academic research | emerging AI agent frameworks |
| Stay updated with major conferences and announcements | AI frameworks conferences announcements 2025 |

---

## Cost Tip

Keep `searches` count low during development (3 is reasonable). Each search costs ~$0.025:

| Searches | Approx. Cost |
|---|---|
| 3 | ~$0.075 |
| 5 | ~$0.125 |
| 10 | ~$0.25 |

---

## Key Takeaways

- `output_type` on an `Agent` enables structured outputs — the agent returns a Pydantic object
- **Field docstrings** are included in the model's context — always annotate your Pydantic fields
- The `reason` field before `query` is a simple but effective chain-of-thought technique
- Structured outputs = JSON under the hood, deserialized into a typed Python object
- The planner is stateless — it plans but does not execute searches

---

## Related Concepts

- Pydantic `BaseModel` and field annotations
- Chain-of-thought prompting
- `output_type` vs `response_format` in OpenAI APIs
- Connecting planner → search agent → synthesis agent (next steps)