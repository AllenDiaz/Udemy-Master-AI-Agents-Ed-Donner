# MCP — When to Build Your Own MCP Server (and When NOT To)

## Overview

Before building a custom MCP server, this lesson establishes the right mental model: when building an MCP server makes sense, and — more importantly — when it doesn't.

---

## Good Reasons to Build an MCP Server

| Reason | Description |
|---|---|
| **Share tools with others** | Package your tools so anyone can plug them into their agent with zero code |
| **Enterprise tool library** | Standardize tools across teams and languages in a consistent, reusable format |
| **Understanding the plumbing** | Educational — learn how MCP works under the hood |

---

## The One Big Reason NOT to Build an MCP Server

> **If you're building tools for your own agent — don't use MCP.**

This is one of the most common MCP misconceptions:

```
❌ Wrong thinking:
"I want to add a tool to my agent → I should build an MCP server"

✅ Right thinking:
"I want to add a tool to my agent → just write the function"
```

### Why MCP is the Wrong Choice for Your Own Tools

```python
# The right way — just a function
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return requests.get(f"https://api.weather.com/{city}").json()

agent = Agent(tools=[get_weather])   # done ✅
```

Adding MCP here would:
- Introduce a **process boundary** (spawn a separate process)
- Add **stdin/stdout communication overhead**
- Create **more moving parts** with nothing gained
- Take a simple function call and turn it into a distributed system call

> **The innovation is the tool itself. MCP is only for sharing tools with others.**

---

## The Rule

| Situation | Use |
|---|---|
| Building tools for **your own** agent | Plain function / decorator — no MCP |
| Using tools written by **someone else** | MCP ✅ |
| Sharing your tools with **other people** | Build an MCP server ✅ |
| Learning how MCP works internally | Build an MCP server ✅ (educational) |

---

## Key Takeaways

- MCP is about **reuse and sharing** — not about how you build tools for yourself
- Building an MCP server for your own internal tools adds complexity with no benefit
- The right time to reach for MCP is when you want to **consume** or **publish** tools across team/system boundaries
- We're building one today anyway — purely to understand the plumbing

---

## Up Next

Building a custom MCP server from scratch — implementing `list_tools` and `call_tool`.