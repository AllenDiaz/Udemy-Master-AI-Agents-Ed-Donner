# MCP Architecture — Diagrams, Transport Types & What MCP Servers Actually Do

## Overview

This lesson goes deep on the MCP architecture — the three deployment patterns, what MCP servers actually do under the hood, and why most MCP servers run locally even when they access remote APIs.

---

## The Full MCP Architecture Diagram

```
Your Computer
┌─────────────────────────────────────────────────────┐
│                    MCP Host                          │
│  (Claude Desktop / Claude Code / Your Agent)         │
│                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌────────┐ │
│  │  MCP Client  │    │  MCP Client  │    │  MCP   │ │
│  │      1       │    │      2       │    │ Client │ │
│  └──────┬───────┘    └──────┬───────┘    └───┬────┘ │
└─────────┼────────────────────┼───────────────┼──────┘
          │                    │               │
          ▼                    ▼               │ (remote)
   ┌─────────────┐    ┌──────────────┐         ▼
   │  MCP Server │    │  MCP Server  │   Remote MCP
   │  (local     │    │  (local      │   Server
   │   process)  │    │   process)   │   (internet)
   └─────────────┘    └──────────────┘
```

**One MCP client per MCP server** — the client lives inside the host process, the server runs separately.

---

## Three MCP Server Deployment Patterns

### Pattern 1 — Local Server, Local Resources (Simplest)

```
Host → MCP Client → MCP Server (local) → Local files/system
```

- Server runs on your machine, uses your local resources
- Example: `@modelcontextprotocol/server-filesystem` — reads/writes your local files
- No internet calls — everything stays on your computer

### Pattern 2 — Local Server, Remote API (Most Common)

```
Host → MCP Client → MCP Server (local) → API call → Internet service
```

- Server runs on your machine, but calls out to an external API
- Examples: Fetch (web pages), weather, stock prices
- **The server describes the API in natural language; the actual data comes from the internet**

### Pattern 3 — Remote Server (Less Common for Agent Builders)

```
Host → MCP Client → Remote MCP Server (someone else's computer)
```

- Server runs on a third party's infrastructure
- Examples: Jira (Atlassian), Context7 (API documentation)
- Most common when connecting to paid/authenticated third-party services
- More common when equipping Claude Desktop/Claude Code than when building your own agents

---

## The Most Important Point — What MCP Servers Actually Do

An MCP server does exactly **two things**:

### 1. List Tools

Returns JSON descriptions of available tools — the same JSON from Week 1:

```json
{
  "name": "get_weather",
  "description": "Get the current weather for a city",
  "parameters": {
    "city": {
      "type": "string",
      "description": "The city to get weather for"
    }
  }
}
```

### 2. Call Tool

Executes a tool when the LLM requests it — most commonly by **making an API request**:

```
LLM: "Call get_weather with city=London"
     ↓
MCP Server: HTTP GET https://api.weather.com/London
     ↓
Returns: {"temp": "15°C", "conditions": "cloudy"}
```

> MCP servers are the **bridge between the natural language world of LLMs and the API world of services**.

---

## The "Local Server" Confusion — Explained

> *"If my MCP server runs locally, how does it get the weather?"*

The answer: **two separate concerns**

| | Runs where | Does what |
|---|---|---|
| MCP server code | Your local machine | Describes the tools in natural language for the LLM |
| Actual functionality | Internet (API call) | Fetches the real data |

The local MCP server **describes** the weather API to the LLM. When called, it **makes a web request** to the weather service. The local code is just the adapter/description layer.

---

## Real-World MCP Server Examples

| MCP Server | Pattern | What it does |
|---|---|---|
| `server-filesystem` | Local → Local | Read/write local files |
| `fetch` | Local → API | Fetch web page content as Markdown |
| Weather server | Local → API | Get weather from weather service API |
| Stock prices | Local → API | Get prices from financial API |
| Jira (Atlassian) | Remote | Access your Jira account via Atlassian's server |
| Context7 | Remote | Get latest API documentation for LLMs |
| Playwright | Local → Local | Drive a local browser instance |

---

## Key Takeaways

- One MCP client per MCP server — always
- **Most MCP servers run locally** even when accessing remote data — the local code is just the description layer
- MCP servers do two things: **list tools** (JSON) and **call tools** (usually an API request)
- Pattern 2 (local server → API call) is the most common pattern when building your own agents
- Pattern 3 (remote servers) is more common for connecting Claude Desktop/Code to paid services
- MCP is the natural language description layer sitting between LLMs and APIs — that's its core value

---

## Up Next

Building your first MCP server — implementing `list_tools` and `call_tool` from scratch.