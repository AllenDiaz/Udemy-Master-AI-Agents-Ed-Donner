# Evaluator-Optimizer Workflow with LLMs (Framework-Free)

## Overview

This lesson demonstrates how to build an **evaluator-optimizer agentic design pattern** by directly calling LLMs — no agentic framework required. The workflow uses **GPT-4 Mini** as the primary agent and **Gemini** as the evaluator.

---

## Key Concepts

- **Evaluator-Optimizer Pattern** — An agentic design pattern where one LLM generates a response and a second LLM evaluates its quality. If the response fails, it is regenerated with feedback.
- **Structured Outputs** — A technique to force an LLM to respond in a predefined JSON schema, which a client library then deserializes into a typed object.
- **Pydantic Models** — Python classes that define data schemas using `BaseModel`. Used here to represent the evaluator's response.
- **Framework-Free Approach** — Building LLM workflows by directly calling APIs, reinforcing understanding of internals without relying on libraries like LangChain.

---

## Important Definitions

| Term | Definition |
|---|---|
| `BaseModel` | Pydantic base class used to define structured data schemas |
| `Structured Outputs` | API feature that constrains LLM responses to a specific JSON/object schema |
| `Evaluator` | A second LLM (Gemini) that judges whether the first LLM's response is acceptable |
| `Rerun` | A function that re-prompts the primary LLM, including the evaluator's rejection feedback |
| Pig Latin | A deliberately bad response format used to demonstrate evaluator rejection |

---

## Step-by-Step Process

### 1. Define the Evaluation Schema (Pydantic)

```python
from pydantic import BaseModel

class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str
```

### 2. Set Up the Evaluator System Prompt

- Instruct the evaluator LLM to assess whether the agent's latest response is professional, engaging, and contextually accurate.
- Provide the evaluator with the same background context given to the primary agent.

### 3. Build the `evaluate()` Function

- Takes: `reply`, `original_message`, `history`
- Calls **Gemini** using the **Structured Outputs** API
- Returns: a populated `Evaluation` object (`is_acceptable`, `feedback`)

```python
# Conceptual structure
response = gemini_client.parse(
    model="gemini-flash",
    messages=[system_msg, user_prompt(reply, message, history)],
    response_format=Evaluation
)
```

### 4. Build the `rerun()` Function

- Triggered when `evaluation.is_acceptable == False`
- Appends a new system instruction: *"Your previous answer was rejected. Here's the feedback: ..."*
- Re-calls the primary LLM (GPT-4 Mini) with this augmented context

### 5. Assemble the Full `chat()` Workflow

```
User Message
     │
     ▼
[GPT-4 Mini] ──► Generate Reply
     │
     ▼
[Gemini Evaluator] ──► is_acceptable?
     │                        │
    YES                       NO
     │                        │
Return Reply           [Rerun with Feedback]
                               │
                               ▼
                        Return New Reply
```

---

## Practical Example

- **Normal flow:** User asks *"What is your current job?"* → GPT-4 Mini responds → Gemini evaluates → ✅ Passes
- **Failure flow:** User asks *"Do you hold a patent?"* → System prompt secretly injects *"Reply in Pig Latin"* → Gemini evaluates → ❌ Rejects ("not professional") → Rerun triggered → ✅ Clean response returned

---

## Key Takeaways

- Structured outputs and **tool use** are closely related — both constrain the LLM's output format.
- This pattern is **commercially applicable**: validate LLM responses in production pipelines.
- You can swap Gemini for any other LLM (OpenAI, Llama, etc.) as the evaluator.
- Building workflows **without a framework** deepens understanding of how agentic systems actually work under the hood.

---

## Related Concepts to Explore

- Structured outputs vs. function/tool calling
- Multi-LLM pipelines
- Pydantic data validation
- Gradio UI integration for LLM apps