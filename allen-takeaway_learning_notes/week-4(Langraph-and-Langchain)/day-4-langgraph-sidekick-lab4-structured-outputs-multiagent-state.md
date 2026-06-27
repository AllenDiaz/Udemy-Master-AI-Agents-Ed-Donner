# LangGraph — Sidekick Lab 4 (Structured Outputs, Multi-Agent State & Worker Node)

## Overview

This lesson builds the core of the **Sidekick project** — a multi-agent LangGraph workflow with a **worker** (task executor) and an **evaluator** (quality checker). Introduces structured outputs on an LLM, a richer state object, and the worker node with dynamic prompting.

---

## Evaluator Output Schema (Structured Output)

```python
from pydantic import BaseModel
from typing import Optional

class EvaluatorOutput(BaseModel):
    feedback: str
    """Feedback on the assistant's response"""

    success_criteria_met: bool
    """Whether the success criteria has been met"""

    user_input_needed: bool
    """True if more input or clarification is needed from the user, or if the assistant is stuck"""
```

---

## Rich State Object

Unlike previous lessons (just `messages`), Sidekick's state carries full workflow context:

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]   # ← reducer: accumulates
    success_criteria: Optional[str]            # ← overwrite: set upfront
    feedback_on_work: Optional[str]            # ← overwrite: from evaluator
    success_criteria_met: bool                 # ← overwrite: evaluator verdict
    user_input_needed: bool                    # ← overwrite: needs clarification?
```

**Reducer vs. overwrite behavior:**
- `messages` has `add_messages` reducer → **accumulates** across nodes
- All other fields have no reducer → **overwrite** with latest value from any node

---

## Two LLMs

```python
from langchain_openai import ChatOpenAI

# Worker — executes tasks, uses browser tools
worker_llm = ChatOpenAI(model="gpt-4o-mini")
worker_llm_with_tools = worker_llm.bind_tools(tools)

# Evaluator — judges worker output, returns structured output
evaluator_llm = ChatOpenAI(model="gpt-4o-mini")
evaluator_llm_structured = evaluator_llm.with_structured_output(EvaluatorOutput)
```

### `with_structured_output()` — LangChain's Structured Output

```python
evaluator_llm.with_structured_output(EvaluatorOutput)
```

- Forces the LLM to respond as a populated `EvaluatorOutput` Pydantic object
- Same concept as OpenAI Agents SDK's `output_type` and CrewAI's `output_pydantic`
- Not all models support this — fallback: prompt for JSON manually and parse it

---

## Worker Node

The worker is the task-executing agent. Its system prompt is dynamically built from state:

```python
def worker(state: State) -> State:
    system_message = f"""You are a helpful assistant that can use tools to complete tasks.
    Keep working until either you have a question for the user, or the success criteria is met.
    Success criteria: {state['success_criteria']}

    Reply with a question if you need clarification (clearly state: "I have a question: ...")
    Or reply with your final answer without asking follow-up questions.
    """

    # If evaluator previously rejected the work, add feedback to system prompt
    if state.get("feedback_on_work"):
        system_message += f"""
        Previously you thought you completed the assignment, but it was rejected.
        Feedback: {state['feedback_on_work']}
        Please continue ensuring you meet the success criteria.
        """

    # Handle existing system messages in conversation history
    messages = inject_or_replace_system_message(state["messages"], system_message)

    response = worker_llm_with_tools.invoke(messages)
    return {"messages": [response]}
```

**Key design choices:**
- `success_criteria` comes from state — set by the user at the start
- If `feedback_on_work` exists in state, the worker knows it was rejected and why
- System message is rebuilt dynamically on every invocation — fresh context each super step
- Returns only `messages` — `add_messages` reducer appends it to history

---

## Multi-Agent Architecture (Preview)

```
User input + success_criteria
        │
        ▼
   [worker node]  ←──────────────────────┐
        │                                │
        ▼                                │
  [tools node]  (if tool call needed)    │
        │                                │
        ▼                                │
  [evaluator node]                       │
        │                                │
   ┌────┴────┐                           │
   ▼         ▼                           │
[END]   [back to worker] ────────────────┘
  (success)  (needs more work / feedback)
```

---

## Key Takeaways

- `with_structured_output(PydanticModel)` gives the evaluator a typed, reliable response format
- State can hold much more than just messages — use it to carry workflow context between nodes
- Fields without reducers are overwritten — use this for flags and single values
- The worker's system prompt is **dynamically constructed from state** — enables feedback loops
- Two separate LLMs with different roles = proper multi-agent separation of concerns
- Prompting the worker to either ask a question OR give a final answer (no "can I help you more?") keeps the evaluator from getting confused

---

## Up Next

Building the evaluator node, worker router, and wiring the full multi-agent graph together.