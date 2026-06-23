# Handoffs — Delegating Control Between Agents

## Overview

This lesson introduces **handoffs**, a distinct construct in the OpenAI Agents SDK for passing full control from one agent to another. It extends the sales email example by adding an **email formatter/sender agent** that the sales manager can delegate to after selecting the best email.

---

## Agents as Tools vs. Handoffs

| | Agents as Tools | Handoffs |
|---|---|---|
| **Control flow** | Request → response → returns to caller | One-way delegation — control does NOT return |
| **Mindset** | Using a feature to help complete a task | Delegating full ownership of a task |
| **Analogy** | Calling a helper function | Handing off a ticket to another team |

> Use **agents as tools** when you need a result back to continue working.  
> Use **handoffs** when you're done and another agent should take it from there.

---

## Architecture: Extended Sales Email Example

```
Sales Manager Agent
├── Tool: sales_agent_one      → generates email variant 1
├── Tool: sales_agent_two      → generates email variant 2
├── Tool: sales_agent_three    → generates email variant 3
└── Handoff: emailer_agent     → formats & sends the chosen email
        ├── Tool: subject_writer     → writes email subject line
        ├── Tool: html_converter     → converts text/markdown to HTML
        └── Tool: send_html_email    → sends via SendGrid
```

---

## New Agents and Tools

### Subject Writer Agent → Tool

```python
subject_writer_agent = Agent(
    instructions="Write a compelling email subject line likely to get a response."
)
subject_tool = subject_writer_agent.as_tool(
    tool_name="subject_writer",
    tool_description="Write a subject for an email"
)
```

### HTML Converter Agent → Tool

```python
html_converter_agent = Agent(
    instructions="Convert a text/markdown email body to a clean, compelling HTML email."
)
html_tool = html_converter_agent.as_tool(
    tool_name="html_converter",
    tool_description="Convert a text email to HTML format"
)
```

### Send HTML Email (Plain Function Tool)

```python
def send_html_email(subject: str, body: str):
    # Sends HTML email via SendGrid to all sales prospects
    ...
```

---

## Creating the Handoff Agent

```python
emailer_agent = Agent(
    name="Email Manager",
    instructions="""
        You are an email formatter and sender.
        You receive the body of an email.
        First use the subject_writer tool, then the html_converter tool,
        then send the email using send_html_email.
    """,
    tools=[subject_tool, html_tool, send_html_email_tool],
    handoff_description="Convert an email to HTML and send it"  # announces this agent to others
)
```

> `handoff_description` is how this agent presents itself to other agents that may want to delegate to it — similar to a tool description.

---

## Connecting It All: Sales Manager with Handoff

```python
sales_manager = Agent(
    name="Sales Manager",
    instructions="...",
    tools=[tool_one, tool_two, tool_three],   # sales agent tools
    handoffs=[emailer_agent]                   # delegation target
)
```

- `tools` — agents/functions the manager calls and gets results back from
- `handoffs` — agents the manager can fully delegate to (no return)

---

## Full Workflow at Runtime

1. Sales manager calls all three sales agent tools → gets three email variants
2. Sales manager picks the best one
3. Sales manager **hands off** to `emailer_agent`
4. Emailer agent calls `subject_writer` tool → gets subject line
5. Emailer agent calls `html_converter` tool → gets HTML body
6. Emailer agent calls `send_html_email` tool → email sent ✅

---

## Key Takeaways

- Handoffs enable **true agent delegation** — not just tool calls
- An agent can have both `tools` (returns control) and `handoffs` (passes control)
- A handoff agent can itself have its own tools — agents compose naturally
- `handoff_description` helps the orchestrator decide when to delegate
- Use traces to visualize the full agent-tool-handoff hierarchy

---

## Related Concepts

- `asyncio.gather()` for running agents in parallel
- Agent-as-tool pattern (`.as_tool()`)
- Multi-agent orchestration patterns
- OpenAI Traces for debugging handoff chains