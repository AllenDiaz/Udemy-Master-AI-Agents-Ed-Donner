# Agents as Tools — Multi-Agent Orchestration with OpenAI Agents SDK

## Overview

This lesson introduces a powerful pattern: **wrapping an agent as a tool**, allowing a higher-level "manager" agent to orchestrate multiple specialized sub-agents dynamically. The example builds a sales manager that generates cold sales emails using three competing sales agents, picks the best, and sends it via email.

---

## Key Concept: Agents as Tools

In addition to wrapping plain functions as tools, you can wrap an **entire agent** as a tool using `.as_tool()`.

```python
tool_one = sales_agent_one.as_tool(
    tool_name="sales_agent_one",
    tool_description="Write a cold sales email"
)
```

**What `.as_tool()` does:**
- Creates a `FunctionTool` with the appropriate JSON schema
- When the tool is called, it **executes the agent** (i.e. makes the LLM call with that agent's instructions)
- Acts as a lightweight wrapper — the agent becomes indistinguishable from any other tool

> Think of it as: **agent → wrapper → tool** that any other agent can call

---

## Architecture: Sales Manager Example

```
Sales Manager Agent (orchestrator)
├── Tool: sales_agent_one    → wraps Sales Agent 1 (LLM call)
├── Tool: sales_agent_two    → wraps Sales Agent 2 (LLM call)
├── Tool: sales_agent_three  → wraps Sales Agent 3 (LLM call)
└── Tool: send_email         → plain Python function (calls SendGrid)
```

---

## Implementation

### Step 1 — Create Agent Tools

```python
tool_one   = sales_agent_one.as_tool(tool_name="sales_agent_one",   tool_description="Write a cold sales email")
tool_two   = sales_agent_two.as_tool(tool_name="sales_agent_two",   tool_description="Write a cold sales email")
tool_three = sales_agent_three.as_tool(tool_name="sales_agent_three", tool_description="Write a cold sales email")

tools = [tool_one, tool_two, tool_three, send_email]
```

### Step 2 — Create the Orchestrator (Manager Agent)

```python
sales_manager = Agent(
    name="Sales Manager",
    instructions="""
        You are a sales manager working for Comply.
        You use the tools given to you to generate cold sales emails.
        You never generate sales emails yourself — you always use the tools.
        You try all three tools once before choosing the best.
        You pick the single best email and use the Send Email tool to send it.
    """,
    tools=tools,
    model="gpt-4o-mini"
)
```

### Step 3 — Run the Workflow

```python
with trace("Sales Manager"):
    result = await Runner.run(sales_manager, "Send a cold sales email addressed to Dear CEO")
```

---

## What Happened at Runtime (from Trace)

1. `sales_agent_one` tool called → sub-agent generates email variant 1
2. `sales_agent_two` tool called → sub-agent generates email variant 2
3. `sales_agent_three` tool called → sub-agent generates email variant 3
4. Sales manager picks the best email
5. `send_email` tool called → email sent via SendGrid

**Total time: ~18 seconds**

---

## Key Takeaways

- `.as_tool()` is a one-liner that converts any agent into a callable tool
- The **orchestrator agent decides** what to run, in what order — no hardcoded Python flow
- This pattern enables true multi-agent systems where agents collaborate dynamically
- The OpenAI Traces dashboard clearly shows the agent-tool hierarchy, making it easy to debug
- Wrapping agents as tools vs. using plain function tools are **interchangeable** from the manager's perspective

---

## Tips

- Be explicit in orchestrator instructions (e.g. "try all three before choosing") — LLMs respond well to clear directives
- Use `trace()` to monitor which agents/tools were called and in what order
- Refactor repetitive `.as_tool()` calls into a loop for cleaner code

---

## Related Concepts

- Agent handoffs (alternative to agents-as-tools for passing control)
- Function tools vs. agent tools
- OpenAI Traces for multi-agent observability
- Mail merge / dynamic prompt personalization