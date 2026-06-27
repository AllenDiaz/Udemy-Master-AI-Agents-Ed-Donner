# LangGraph — Sidekick Class Internals (Worker, Evaluator, build_graph & run)

## Overview

This lesson walks through the complete `Sidekick` class implementation — the worker node with refined prompts, the evaluator node with trust adjustments, `build_graph()`, and `run_super_step()`.

---

## Worker Node — Prompt Engineering Insights

The worker's system prompt was refined through experimentation. Key additions:

### 1. Inject Current Date/Time Directly

```python
system_message = f"""
You are a helpful assistant that can use tools to complete tasks.
Current date and time: {datetime.now().strftime("%Y-%m-%d %H:%M")}
...
"""
```

> Don't make date/time a tool — it's a **resource** (static info), not an action. Always injecting it is simpler and more reliable than prompting the agent to call a tool for it.

### 2. Python REPL Print Statement Hint

```python
system_message += """
You have a tool to run Python code. Note: you must include a print() statement
if you want to receive output from the tool.
"""
```

Without this hint, `gpt-4o-mini` didn't include `print()` in generated code, causing it to loop repeatedly getting no results. One line in the prompt fixed it immediately.

> This is a perfect example of prompt engineering R&D — model-specific behavior that requires targeted fixes.

### 3. Feedback Injection (Same as Notebook)

```python
if state.get("feedback_on_work"):
    system_message += f"""
    Previously your reply was rejected. Feedback: {state['feedback_on_work']}
    Please try again meeting the success criteria.
    """
```

---

## Evaluator Node — Trust Calibration

The evaluator was too harsh — rejecting work even when the agent correctly used tools. Fix:

```python
evaluator_prompt += """
The assistant has access to tools including file writing. If the assistant says 
they've written a file, assume they have done so. Give the assistant the benefit 
of the doubt if they say they completed something — but reject if more work is needed.
"""
```

> Calibrating evaluator strictness is an ongoing R&D process. Too strict = infinite loops. Too lenient = low quality output. Add concrete examples to the prompt to guide the balance.

---

## `build_graph()` Method

```python
def build_graph(self):
    graph_builder = StateGraph(State)

    graph_builder.add_node("worker", self.worker)
    graph_builder.add_node("tools", ToolNode(tools=self.tools))
    graph_builder.add_node("evaluator", self.evaluator)

    graph_builder.add_edge(START, "worker")
    graph_builder.add_conditional_edges("worker", self.worker_router,
        {"tools": "tools", "evaluator": "evaluator"})
    graph_builder.add_edge("tools", "worker")
    graph_builder.add_conditional_edges("evaluator", self.route_based_on_evaluation,
        {"worker": "worker", END: END})

    memory = MemorySaver()
    self.graph = graph_builder.compile(checkpointer=memory)
```

---

## `run_super_step()` Method

```python
async def run_super_step(self, user_message: str, success_criteria: str = "") -> dict:
    config = {"configurable": {"thread_id": self.sidekick_id}}

    initial_state = {
        "messages": [{"role": "user", "content": user_message}],
        "success_criteria": success_criteria or "The answer should be clear and accurate.",
        "feedback_on_work": None,
        "success_criteria_met": False,
        "user_input_needed": False
    }

    result = await self.graph.ainvoke(initial_state, config=config)

    return {
        "user_message": user_message,
        "reply": result["messages"][-2].content,      # worker's answer
        "evaluation": result["messages"][-1].content  # evaluator's verdict
    }
```

- Default success criteria: `"The answer should be clear and accurate."` — used when user doesn't provide one
- Returns both the worker reply and evaluator feedback for display in UI

---

## `cleanup()` Method

```python
async def cleanup(self):
    if self.browser:
        await self.browser.close()
    if self.playwright:
        await self.playwright.stop()
```

> ⚠️ Browser resource management is ongoing — each new `Sidekick()` instance spawns a new browser. Ensure `cleanup()` is always called when done to avoid orphaned browser processes.

---

## Key Prompt Engineering Lessons

| Issue | Fix |
|---|---|
| Agent didn't know current date | Inject datetime into system prompt directly |
| Python REPL returned no output | Add "include print() for output" hint |
| Evaluator rejected correct work | Add "give benefit of the doubt" instruction |
| Evaluator looped on same mistake | Add "if already given this feedback, request user input" |
| Inconsistent tool behavior | Add concrete examples in prompt |

> There are no universal rules — every model, task, and tool combination may need different prompt adjustments. Document what works and iterate.

---

## Key Takeaways

- Notebook prototyping → Python class is a clean production pattern for AI engineering
- Current date/time is a **resource**, not a tool — inject it directly into the prompt
- Model-specific quirks (like the `print()` issue) require targeted prompt fixes
- Evaluator trust calibration is a constant balancing act — too strict = loops, too lenient = poor quality
- `build_graph()` and `run_super_step()` cleanly separate graph definition from execution
- Browser resource cleanup is important — always call `cleanup()` after use

---

## Up Next

Building `app.py` — the Gradio entry point that ties everything together.