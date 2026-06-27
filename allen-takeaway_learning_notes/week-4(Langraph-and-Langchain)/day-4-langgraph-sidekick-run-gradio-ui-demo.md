# LangGraph — Running the Sidekick (Gradio UI & End-to-End Demo)

## Overview

This lesson completes the Sidekick project by building the Gradio UI, running the full multi-agent workflow end-to-end, and verifying the trace in LangSmith.

---

## Thread ID — Multi-User Support

```python
import random

thread_id = str(random.randint(1, 1_000_000_000))
```

A random thread ID is generated each time the UI launches — ensuring:
- Each Gradio session has isolated memory
- Multiple users can run the sidekick simultaneously with separate conversations
- No bleed-over from previous sessions

---

## `process_message` — Async Gradio Callback

```python
async def process_message(user_message: str, success_criteria: str, history: list):
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "messages": [{"role": "user", "content": user_message}],
        "success_criteria": success_criteria,   # passed to evaluator throughout
        "feedback_on_work": None,
        "success_criteria_met": False,
        "user_input_needed": False
    }

    result = await graph.ainvoke(initial_state, config=config)

    # Show both worker response and evaluator feedback in UI
    assistant_reply = result["messages"][-2].content   # worker's answer
    evaluator_reply = result["messages"][-1].content   # evaluator's verdict

    return history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": assistant_reply},
        {"role": "assistant", "content": evaluator_reply}
    ]
```

> `success_criteria` is set once at the start and flows through all nodes via state — the evaluator reads it on every pass.

---

## Gradio UI

```python
import gradio as gr

with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Sidekick — Personal Coworker")
    chatbot = gr.Chatbot(type="messages")
    user_input = gr.Textbox(label="Your request")
    success_input = gr.Textbox(label="Success criteria")
    go_btn = gr.Button("Go", variant="primary")
    reset_btn = gr.Button("Reset")

    go_btn.click(process_message, [user_input, success_input, chatbot], chatbot)
    reset_btn.click(lambda: ([], "", ""), None, [chatbot, user_input, success_input])

demo.launch()
```

---

## Live Demo

**Request:** *"What is the current USD/GBP exchange rate?"*  
**Success criteria:** *"An accurate answer"*

### What Happened (LangSmith trace)

1. `worker` → called `navigate_browser` → exchange rate page
2. `worker` → called `get_elements` → parsed page structure
3. `worker` → called `extract_text` → found rate: **0.77463**
4. `evaluator` → assessed response → provided feedback

**Worker response:** "The current USD to GBP exchange rate is approximately 0.77463."

**Evaluator feedback:** "The assistant provided an approximate rate. However, it should ideally note that rates change frequently." — still returned control to user.

**Cost:** ~19,000 tokens → **0.2 cents** for the full interaction.

---

## LangSmith Trace — What Was Visible

```
worker → navigate_browser
worker → get_elements
worker → extract_text
worker → (done, no tool call)
evaluator → assessed with structured output
route_based_on_evaluation → END
```

Evaluator's full prompt was visible in LangSmith:
- System: evaluator role instructions
- Human: formatted conversation + success criteria + final response
- Response: JSON conforming to `EvaluatorOutput` schema

---

## Key Takeaways

- Random `thread_id` per session enables multi-user support out of the box
- `success_criteria` flows through the entire state — set once, available everywhere
- Both worker response and evaluator feedback shown in UI — useful for debugging
- The evaluator-optimizer loop can run many times on harder tasks (observed: 25 messages in some tests)
- LangSmith makes the full agent trace inspectable — essential for prompt debugging
- Total cost for a full Playwright + evaluator run: **~0.2 cents**

---

## Sidekick Project — Complete Feature Summary

| Feature | Implementation |
|---|---|
| Browser automation | Playwright via `PlaywrightBrowserToolkit` |
| Push notifications | Custom tool via Pushover |
| Task evaluation | Evaluator LLM with `with_structured_output()` |
| Feedback loop | Worker re-runs with evaluator feedback in state |
| Memory | `MemorySaver` with random thread IDs |
| Observability | LangSmith tracing |
| Multi-user support | Random thread ID per Gradio session |

---

## Up Next

Packaging the Sidekick as a proper Python application with more features.