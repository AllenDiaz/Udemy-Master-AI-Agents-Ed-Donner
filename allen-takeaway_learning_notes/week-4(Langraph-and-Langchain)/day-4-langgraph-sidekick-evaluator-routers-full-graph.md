# LangGraph — Sidekick Evaluator Node, Routers & Full Multi-Agent Graph

## Overview

This lesson completes the Sidekick's multi-agent graph by building the **evaluator node**, two **router functions**, and wiring everything together into a full agentic workflow with a feedback loop.

---

## Worker Router

Decides where to route after the worker runs:

```python
def worker_router(state: State) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"       # worker wants to call a tool
    return "evaluator"       # worker produced an answer — evaluate it
```

---

## Evaluator Node

Assesses the worker's response against the success criteria:

```python
def evaluator(state: State) -> State:
    last_response = state["messages"][-1].content

    system_prompt = """You are an evaluator that determines if a task has been completed 
    successfully by an assistant. Assess the last response based on the success criteria.
    Respond with feedback and decide:
    - Is the success criteria met?
    - Is more user input needed (question from assistant, needs clarification, or stuck)?
    """

    user_prompt = f"""
    Conversation so far:
    {format_conversation(state["messages"])}

    Success criteria: {state["success_criteria"]}

    Final response to evaluate: {last_response}

    Respond with your feedback. If the assistant is repeating the same mistakes, 
    consider responding that user input is required.
    """

    # Add prior feedback context if this isn't the first evaluation
    if state.get("feedback_on_work"):
        user_prompt += f"""
        Note: In a prior attempt you already provided this feedback: {state["feedback_on_work"]}
        If the assistant is repeating mistakes, flag that user input is required.
        """

    evaluator_messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    result: EvaluatorOutput = evaluator_llm_structured.invoke(evaluator_messages)

    return {
        "messages": [AIMessage(content=f"Evaluator feedback: {result.feedback}")],
        "feedback_on_work": result.feedback,
        "success_criteria_met": result.success_criteria_met,
        "user_input_needed": result.user_input_needed
    }
```

**Key prompting decisions:**
- Explicitly pass the full conversation AND the final response — makes it clear what's being evaluated
- Repeat the field descriptions from the Pydantic schema in the prompt — repetition biases the model
- Add context if evaluator has already provided feedback — prevents infinite loops on the same mistake
- These prompt choices came from experimentation, not rules — this is AI engineering R&D

---

## Evaluation Router

Decides where to route after the evaluator runs:

```python
def route_based_on_evaluation(state: State) -> str:
    if state["success_criteria_met"] or state["user_input_needed"]:
        return END    # done (success) or needs human (stuck/question)
    return "worker"   # not done, no blocker — send back to worker with feedback
```

---

## Full Graph Assembly

```python
graph_builder = StateGraph(State)

# Nodes
graph_builder.add_node("worker", worker)
graph_builder.add_node("tools", ToolNode(tools=tools))
graph_builder.add_node("evaluator", evaluator)

# Edges
graph_builder.add_edge(START, "worker")

graph_builder.add_conditional_edges(
    "worker",
    worker_router,
    {"tools": "tools", "evaluator": "evaluator"}
)

graph_builder.add_edge("tools", "worker")   # tool result → back to worker

graph_builder.add_conditional_edges(
    "evaluator",
    route_based_on_evaluation,
    {"worker": "worker", END: END}
)

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
```

---

## Graph Visualization

```
START
  │
  ▼
[worker] ──── worker_router ──── tool_call? ──── [tools]
  ▲                                                  │
  │ (feedback loop)                                  │
  │◄──── route_based_on_evaluation ◄──── [evaluator]─┘
                    │
                    ▼
                   END
          (success OR user needed)
```

- **Solid lines** = always taken
- **Conditional lines** = only if condition is true
- The `worker → evaluator → worker` loop can repeat until success or the agent is stuck

---

## Agentic Pattern at Work

This graph implements the **evaluator-optimizer** pattern from Week 1 — now as a proper LangGraph multi-agent workflow:

| Component | Role |
|---|---|
| Worker | Executes the task using tools |
| Tools node | Runs Playwright browser + push notification |
| Evaluator | Judges output against success criteria |
| Worker router | Routes to tools or evaluator |
| Evaluation router | Routes to END or back to worker |

> The loop can run indefinitely — the agent has true autonomy over how many attempts it makes.

---

## Key Takeaways

- Two routers = two conditional edges = the entire control flow of the agent
- The evaluator uses `with_structured_output()` — reliable, typed feedback every time
- Prior feedback is injected back into the evaluator prompt — prevents infinite retry loops
- The `tools → worker` back edge is always required when using a ToolNode
- Prompt iteration is normal — this graph's prompts were refined through testing, not derived from rules
- This is a true agentic loop: it keeps going until either success or it needs help

---

## Up Next

Running the Sidekick end-to-end and seeing the full evaluator-optimizer loop in action.