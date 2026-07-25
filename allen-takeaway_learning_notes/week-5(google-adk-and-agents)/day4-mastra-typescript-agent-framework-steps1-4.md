# Mastra — TypeScript Agent Framework (Steps 1–4)

## Overview

Day 4 of Week 5 introduces **Mastra** — the only TypeScript framework in the course. Same 5 steps, different language and toolchain. No Python notebooks; each step is a separate TypeScript file run via `npm run step<N>`.

---

## Setup

```bash
# Verify Node version (requires v24+)
node --version

# Install dependencies
cd week5/4_mastra
npm install
```

> If Node is below v24, use NVM (`nvm install 24`) or follow `setup_node.md`.

---

## Project Structure

```
week5/4_mastra/
├── board.ts          # SQLite to-do board (TypeScript)
├── tools.ts          # Tool definitions + MCP client
├── step1.ts          # Create agent
├── step2.ts          # Run agent
├── step3.ts          # Add tools
├── step4.ts          # Add MCP
├── step5.ts          # Agent loop with goal
└── lab.md            # Lab instructions (no .ipynb this day)
```

---

## `board.ts` — SQLite To-Do Board (TypeScript)

Same SQLite to-do board as Python labs — just TypeScript SQL queries. Not important to understand deeply, just know it wraps the same read/write functionality.

---

## `tools.ts` — Tool and MCP Definitions

### Function Tools (Mastra style)

```typescript
import { createTool } from "@mastra/core";
import { z } from "zod";   // Zod for input schema validation

const showTodos = createTool({
    id: "show_todos",
    description: "Show the current to-do list and status of all tasks.",
    inputSchema: z.object({}),
    execute: async () => board.listTodos()
});

// Similar for planSteps, completeTask
export const boardTools = [showTodos, planSteps, completeTask];
```

**Key difference from Python:** Mastra uses `createTool()` with an explicit `inputSchema` (Zod) — slightly more verbose than plain Python functions.

### MCP Client

```typescript
import { MCPClient } from "@mastra/mcp";

export function makeFileSystem() {
    return new MCPClient({
        servers: {
            filesystem: {
                command: "npx",
                args: ["-y", "@modelcontextprotocol/server-filesystem", "./workspace"]
            }
        }
    });
}
```

---

## Step 1 — Create an Agent

```typescript
// step1.ts
import { Agent } from "@mastra/core/agent";

const agent = new Agent({
    id: "assistant",
    name: "Assistant",
    instructions: "You are a concise friendly assistant. Reply in a single short sentence.",
    model: "openai/gpt-4o-mini"   // provider/model-name format
});

console.log("Created agent:", agent.name);
```

```bash
npm run step1
# → "Created agent: Assistant"
```

---

## Step 2 — Run the Agent

```typescript
// step2.ts
const response = await agent.generate("Say hello in Spanish");
console.log(response.text);
```

```bash
npm run step2
# → "Hola"
```

> `agent.generate()` — Mastra's equivalent of `agent.run()` / `agent.arun()`.

---

## Step 3 — Add Tools

```typescript
// step3.ts
import { boardTools } from "./tools";
import { resetBoard, addGoal } from "./board";

resetBoard();
addGoal("Read notes.txt and translate its contents.");

const boardAgent = new Agent({
    id: "board-agent",
    name: "Board Agent",
    instructions: "You help manage a shared to-do board.",
    model: "openai/gpt-4o-mini",
    tools: boardTools   // same pattern as Python frameworks
});

const response = await boardAgent.generate("What's on the board right now?");
```

```bash
npm run step3
# → "There is 1 item: Read notes.txt and translate its contents."
```

---

## Step 4 — Add MCP

```typescript
// step4.ts
import { makeFileSystem } from "./tools";

const mcp = makeFileSystem();
const mcpTools = await mcp.getTools();   // get tool list from MCP server

const fileAgent = new Agent({
    id: "file-agent",
    name: "File Agent",
    instructions: "You can read and write files in your workspace.",
    model: "openai/gpt-4o-mini",
    tools: mcpTools
});

const response = await fileAgent.generate("Read notes.txt and summarize it in one short sentence.");
```

```bash
npm run step4
# → "The notes say the team is building a small language tutor."
```

---

## Python vs TypeScript — Syntax Comparison

| Step | Python (Pydantic AI / Agno) | Mastra (TypeScript) |
|---|---|---|
| Agent class | `Agent(...)` | `new Agent({...})` |
| System prompt | `instructions=` | `instructions:` |
| Model | string or object | `"provider/model"` string |
| Run | `agent.run()` / `agent.arun()` | `agent.generate()` |
| Tool definition | Plain function | `createTool({id, description, schema, execute})` |
| MCP | Context manager / toolset | `new MCPClient({servers: {...}})` |
| Schema | Auto from docstring | Explicit Zod schema |

---

## Key Takeaways

- Same 5-step pattern — different language, same concepts
- `agent.generate()` = Mastra's run method
- Tools require explicit Zod schema — more verbose than Python's docstring approach
- MCP client pattern is clean — `await mcp.getTools()` fetches the tool list
- TypeScript's type system adds safety but also more boilerplate
- No Jupyter notebooks for TypeScript — each step is a separate `.ts` file run via `npm run`

---

## Up Next

Step 5 — Agent in a loop with a goal, then the Week 5 project: the meta agent loop.