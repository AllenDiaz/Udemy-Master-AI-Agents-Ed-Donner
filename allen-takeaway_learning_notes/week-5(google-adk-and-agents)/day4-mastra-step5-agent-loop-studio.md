# Mastra — Step 5 (Agent Loop) & Mastra Studio

## Overview

This lesson completes the Mastra lab with Step 5 — running an agent in a loop with a goal — and introduces **Mastra Studio**, the built-in developer UI (similar to ADK Web).

---

## Step 5 — Agent in a Loop with a Goal

```typescript
// step5.ts
import { Agent } from "@mastra/core/agent";
import { boardTools, makeFileSystem } from "./tools";
import { resetBoard, addGoal } from "./board";

const goal = "Read notes.txt, translate its contents into Spanish, write to spanish.txt";
resetBoard();
addGoal(goal);

const fileSystem = makeFileSystem();
const mcpTools = await fileSystem.getTools();

const worker = new Agent({
    id: "worker",
    name: "Worker",
    instructions: `You have a to-do board and file tools. 
                   Take the goal off your board and complete it.`,
    model: "openai/gpt-4o-mini",
    tools: [
        ...boardTools,       // spread board tools
        ...mcpTools          // spread MCP file system tools
    ]
});

const response = await worker.generate("Please work the pending goal on the board.");
```

```bash
npm run step5
```

**What happened:**
1. Goal seeded to SQLite board
2. Agent read goal via `show_todos`
3. `plan_steps` → sub-steps created
4. MCP `read_file` → read `notes.txt`
5. MCP `write_file` → wrote `spanish.txt`
6. `complete_task` → all steps crossed off ✅

---

## Combining Tools in TypeScript

```typescript
tools: [
    ...boardTools,   // spread operator — combines arrays
    ...mcpTools
]
```

> TypeScript spread operator (`...`) is the equivalent of Python's `tools + mcp_tools` list concatenation.

---

## Mastra Studio — Dev UI

```bash
# Launch Mastra Studio (from week5/4_mastra directory)
npm run dev
# → Opens at http://localhost:4111
```

**What you see:**
- List of defined agents
- Chat interface to interact with any agent
- Tool call visualization
- Similar to ADK Web but for TypeScript/Mastra

---

## Day 4 Recap — Mastra vs Python Frameworks

| Concept | Python frameworks | Mastra (TypeScript) |
|---|---|---|
| Agent run | `agent.run()` / `agent.arun()` | `agent.generate()` |
| Tool definition | Plain function + docstring | `createTool({id, description, schema, execute})` |
| Schema | Auto from type hints | Explicit **Zod** schema |
| MCP | Toolset / context manager | `new MCPClient({servers: {...}})` |
| Combine tools | `tools + mcp_tools` | `[...boardTools, ...mcpTools]` |
| Dev UI | ADK Web (`uv run adk web`) | Mastra Studio (`npm run dev`) |
| Package manager | `uv` | `npm` |
| Step runner | `uv run worker.py` | `npm run step5` |

---

## Week 5 — All 6 Frameworks Summary

| Framework | Language | Unique Feature | Run Method |
|---|---|---|---|
| OpenAI Agents SDK | Python | Guardrails, handoffs | `Runner.run()` |
| Google ADK | Python | ADK Web UI, A2A | `runner.run_async()` |
| Pydantic AI | Python | Type safety, structured outputs | `agent.run()` |
| MAF | Python + .NET | LangGraph-like workflows, .NET | `agent.run()` |
| Agno | Python | ~3μs startup, AgentOS | `agent.arun()` |
| **Mastra** | **TypeScript** | **TypeScript/JS ecosystem, Studio UI** | `agent.generate()` |

---

## Key Takeaways

- Mastra follows the exact same 5-step pattern — just TypeScript syntax
- Zod schemas replace Python's docstring/type hint approach for tool definitions
- Spread operator (`...`) combines tool arrays — same as Python list concatenation
- Mastra Studio = ADK Web equivalent for TypeScript
- **All 6 frameworks confirmed: same pattern, different syntax**
- Pick the framework that fits your team's language preference and tooling needs

---

## Up Next

Day 5 — **The Agent Loop Project**: a meta-loop that calls all agents built this week, wrapped in a consumer app.