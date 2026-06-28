# LangGraph — Sidekick Final Run (41 Tools, Human-in-the-Loop & Real Tasks)

## Overview

This lesson runs the complete Sidekick application end-to-end — demonstrating 41 tools, a real LangGraph middleware graph, human-in-the-loop approval, and two real-world tasks: fetching a Hacker News headline and researching flights.

---

## Sidekick Setup

```python
sidekick = Sidekick()
await sidekick.setup()
# → "Set up with 41 tools"
```

### Tool Breakdown

| Category | Tools |
|---|---|
| Playwright browser | navigate, click, extract text, get elements, hyperlinks, etc. |
| Web search | SerpAPI |
| Knowledge | Wikipedia |
| File system | FileManagementToolkit (sandboxed directory) |
| Notifications | Push notification (Pushover) |
| Code execution | Python REPL (⚠️ unsandboxed) |

---

## The Graph at Scale

When using LangGraph's `create_react_agent` (middleware), the compiled graph is significantly more complex than what was built manually:

```
START
  │
  ▼
[middleware] → [more middleware] → [model]
                                      │
                              conditional edges
                                      │
                              human-in-the-loop
                                      │
                                   [tools]
                                      │
                                    END
```

> This is why high-level abstractions like `create_react_agent` exist — building this graph manually line by line would be extremely tedious. The graph still runs LangGraph under the hood.

---

## Live Demo 1: Hacker News Top Story

**Request:** *"Go to news.ycombinator.com and tell me the title of the current top story."*  
**Success criteria:** *"The reply names a specific story currently on the Hacker News front page."*

**What happened:**
1. Agent opened browser → navigated to `news.ycombinator.com`
2. Extracted page content
3. Returned: *"The current top story is: [specific headline]"*
4. Evaluator: *"Matches success criteria — success."* ✅

---

## Live Demo 2: Flight Research Task

**Request:**
> *"Find me the best round-trip flight from New York to London, leaving in about a month, returning a week later. Care about price first, then journey time. Avoid 2+ stops. Write top 3 recommendations to flights.md and send me a push notification with your top pick."*

**Success criteria:** *"flights.md written with three specific options."*

### What the Agent Did (To-Do List via LangSmith)

```
✅ Search Google Flights — round trip NYC → LDN
✅ Identify top 3 flight options
🔄 Write recommendations to flights.md  (in progress)
⏳ Send push notification               (pending — awaiting approval)
```

### Human-in-the-Loop Moment

The agent **paused before sending the push notification** — waiting for human approval. After approving:
- Push notification received: *"Top pick: IcelandAir — $748 round trip"* ✅
- `sandbox/flights.md` created with 3 recommendations ✅
- Evaluator: *"Task completed successfully."* ✅

---

## Key Observations

### Human-in-the-Loop
The graph paused autonomously before a side-effect action (sending a notification) — a key LangGraph feature. The agent resumed after human approval via `sidekick.resume()`.

### To-Do List Behavior
The agent maintained and displayed a live to-do list while working through the flight task — mirroring the agent loop pattern from Week 1's standalone loop demo.

### Evaluator at Work
Both tasks passed evaluation on the first attempt — indicating well-calibrated prompts from prior refinement.

---

## Key Takeaways

- 41 tools = just a list — every added tool is immediately available to the agent
- `create_react_agent` generates a complex LangGraph graph automatically — inspect it with `sidekick.graph.get_graph()`
- Human-in-the-loop pauses are first-class citizens in LangGraph — not bolted on
- The file management toolkit lets the agent write real files to a sandboxed directory
- The evaluator-optimizer loop ensures quality without human review of every step
- Real tasks (flight research, news scraping) work end-to-end — this has genuine business value

---

## Sidekick — Complete Feature Set

| Feature | Details |
|---|---|
| Tools | 41 tools: browser, search, Wikipedia, files, Python, push notification |
| Memory | `MemorySaver` with unique thread ID per session |
| Evaluation | LLM evaluator with `with_structured_output()` |
| Feedback loop | Worker retries with evaluator feedback |
| Human-in-the-loop | Pauses before side-effect actions for approval |
| Observability | LangSmith tracing |
| UI | Gradio with success criteria input |

---

## Up Next

Week 5 — AutoGen framework.