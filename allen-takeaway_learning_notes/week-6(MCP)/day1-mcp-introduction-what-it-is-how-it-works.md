# MCP (Model Context Protocol) — What It Is and How It Works

## Overview

This lesson introduces **MCP (Model Context Protocol)** — Anthropic's standard for connecting tools, resources, and prompts to AI agents. The week's most important topic, finally covered in depth.

---

## What MCP Is NOT

- ❌ Not an agent framework
- ❌ Not a new way to code agents
- ❌ Not a fundamental change to how agents work
- ❌ Not the tools themselves — just the standard for connecting to them

---

## What MCP IS

> **MCP is a protocol — an agreed standard for integrating tools into your agent.**

The **USB-C port for AI applications** (Anthropic's own analogy):
- Universal connector — plug any MCP-compatible tool into any MCP-compatible agent
- Plug-and-play — no custom drivers or glue code needed
- Works across any framework — not tied to LangChain or any specific ecosystem

---

## MCP Covers Three Things (But One Dominates)

| Component | Adoption |
|---|---|
| **Tools** | 🔥 Massively adopted — what everyone uses MCP for |
| Resources | Sometimes used |
| Prompts | Rarely used in practice |

> In the real world: MCP = tools. Everything else is mostly academic.

---

## Why MCP Exists — The Problem It Solves

**Before MCP:**
- LangChain had its own tools ecosystem — only usable within LangChain
- No universal way to share tools across frameworks
- Every integration required custom code

**After MCP:**
- Any tool built to the MCP standard works with any MCP-compatible host
- An agreed standard → massive ecosystem → thousands of tools available immediately

> Analogy: HTTP and HTML are "just standards" — but they gave us the internet. Agreed standards matter.

---

## Honest MCP Skepticism

| Reason to be cautious | Why |
|---|---|
| MCP is just the spec | The real innovation is in the tools themselves (e.g. Playwright by Microsoft) |
| LangChain already had tools | MCP isn't the only ecosystem |
| Easy to make your own tools | MCP mainly helps with *other people's* tools, not your own |
| Wild West ecosystem | So many MCP tools it's hard to find the right one |

---

## The Three MCP Components

### MCP Host

The software application that needs tools — your agent, Claude Desktop, ChatGPT, etc.

```
MCP Host = your agent / your application
```

### MCP Client

A piece of code that runs **inside** the host, connecting it to an MCP server. One client per server.

```
MCP Client = bridge code (often handled by your agent framework)
```

### MCP Server

A separate process containing the actual tools, written by a third party.

```
MCP Server = Microsoft's Playwright tools, Anthropic's Fetch, etc.
```

---

## How They Connect

```
┌─────────────────────────────────────┐
│           MCP Host                  │
│  (your agent / ChatGPT / Claude AI) │
│                                     │
│   ┌─────────────┐                   │
│   │ MCP Client  │ ──── connects ──► │ MCP Server (separate process)
│   │ (one per    │                   │ (Playwright, Fetch, filesystem, etc.)
│   │  server)    │                   │
│   └─────────────┘                   │
└─────────────────────────────────────┘
```

**Key point:** MCP server runs in a **separate process** — isolated from your agent code.

---

## How Agent Frameworks Handle MCP

You don't need to manually create MCP clients — frameworks do it for you:

```python
# You just specify which server you want
tools = MCPToolset(server="filesystem", path="./workspace")

# Framework automatically:
# 1. Creates the MCP client
# 2. Connects to the MCP server
# 3. Retrieves available tools
# 4. Makes them available to your agent
```

---

## MCP History

| Event | Detail |
|---|---|
| Created by | Anthropic |
| Purpose | Universal tool connectivity standard for AI |
| Current steward | Agentic AI Foundation (under Linux Foundation) |
| Status | Open source, community-owned |

---

## Key Takeaways

- MCP = a standard/protocol, not a framework or implementation
- The USB-C analogy is apt — universal plug-and-play for tools
- In practice: MCP = tools (resources and prompts are rarely used)
- MCP solves the cross-framework tool reuse problem
- Agent frameworks handle MCP client creation automatically
- The real innovation is in the tools themselves — MCP just makes them easy to share and reuse
- Being an agreed standard is genuinely important — like HTTP for the web

---

## Up Next

MCP in practice — host/client/server diagrams, transport types, and building your first MCP server.