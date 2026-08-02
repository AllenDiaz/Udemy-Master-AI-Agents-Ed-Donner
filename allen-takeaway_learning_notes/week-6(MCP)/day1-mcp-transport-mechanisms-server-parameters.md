# MCP Transport Mechanisms & Server Parameters

## Overview

This lesson covers the two MCP transport mechanisms (STDIO and Streamable HTTP), the three server deployment patterns, and how MCP server parameters work in practice.

---

## The Two Transport Mechanisms

### 1. STDIO (Standard Input/Output) — Most Common

```
MCP Client → spawns a process → connects via stdin/stdout
```

- Client launches a local program (Python, JavaScript, or Docker)
- Communicates by writing to stdin and reading from stdout
- Like typing commands in a terminal and reading the output
- **Used for: local MCP servers**

### 2. Streamable HTTP

```
MCP Client → HTTP request → MCP Server (local or remote)
```

- Connects over HTTP — supports streaming responses
- Replaced the older SSE (Server-Sent Events) transport
- **Used for: remote MCP servers (required) or local servers (optional)**

---

## Simple Rule: Which Transport to Use

| Server location | Transport to use |
|---|---|
| **Local server** | STDIO (almost always) or Streamable HTTP |
| **Remote server** | Streamable HTTP (required — can't spawn a remote process) |

> 95% of the time when building your own agents: **local server + STDIO**.

---

## MCP Server Parameters

When configuring an MCP server, you provide a **parameters object** that tells the MCP client how to connect.

### STDIO Parameters (local Python server)

```python
# Anthropic's Fetch MCP server (Python)
{
    "command": "uvx",
    "args": ["mcp-server-fetch"]
}
```

### STDIO Parameters (local JavaScript server)

```python
# Playwright MCP server (JavaScript/Node)
{
    "command": "npx",
    "args": ["@playwright/mcp@latest"]
}
```

### Streamable HTTP Parameters (remote server)

```python
# Context7 remote MCP server
{
    "url": "https://mcp.context7.com/mcp"
}
```

> Parameters aren't mystical — they're just instructions for how to launch or connect to the MCP server.

---

## Three Types of Local Programs

| Type | Launcher | Example |
|---|---|---|
| **Python program** | `uvx` | `uvx mcp-server-fetch` |
| **JavaScript/TypeScript** | `npx` | `npx @playwright/mcp@latest` |
| **Docker container** | `docker run` | Less common but valid |

### Why `uvx` and `npx`?

Both install and run a package in an **isolated environment** — no dependency conflicts, guaranteed to work:

```bash
uvx = uv tool run    # Python equivalent
npx = npm package run # Node equivalent
```

This is why STDIO parameters look the way they do — they're just clean, isolated program launchers.

---

## Putting It All Together

```
MCP Host (your agent)
    │
    ├── MCP Client 1 ──STDIO──► uvx mcp-server-fetch      (Python, local)
    │
    ├── MCP Client 2 ──STDIO──► npx @playwright/mcp@latest (JS, local)
    │
    └── MCP Client 3 ──HTTP───► https://mcp.context7.com  (remote)
```

---

## MCP Parameters in Practice

These parameters can be dropped into:
- **Claude Desktop** / Claude Code config
- **Codex** or any AI coding tool
- **Any agent framework** (`MCPToolset`, `MCPServerStdio`, `MCPClient`, etc.)

The framework reads the parameters and:
1. Creates an MCP client
2. Spawns the process (STDIO) or makes HTTP connection
3. Calls `list_tools` → gets available tools
4. Provides them to the agent automatically

---

## Key Takeaways

- **STDIO** = spawn a local process, communicate via stdin/stdout — simple and most common
- **Streamable HTTP** = connect via HTTP — required for remote servers
- `uvx` = Python MCP server launcher; `npx` = JavaScript MCP server launcher
- MCP parameters are just config — not magical, just tell the client how to connect
- Remote servers require HTTP; local servers almost always use STDIO
- The same parameters work across all agent frameworks and AI tools

---

## Up Next

MCP in the lab — connecting real MCP servers to agents and building your first custom MCP server.