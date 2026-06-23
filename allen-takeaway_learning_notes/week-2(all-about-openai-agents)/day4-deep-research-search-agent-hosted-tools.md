# Deep Research — Building a Search Agent with Hosted Tools

## Overview

Day 4, Week 2 kicks off the first large-scale agentic project: a **deep research agent** that searches the web, synthesizes results, and produces a structured report. This lesson covers the first component — the **search agent** — and introduces **hosted tools** provided by OpenAI.

---

## What Is Deep Research?

A classic agentic use case where an agent:
1. Takes a research topic from the user
2. Performs multiple web searches autonomously
3. Synthesizes the results into a coherent report

> This mirrors OpenAI's own "Deep Research" button in ChatGPT — we're building our own version from scratch.

**Business applicability:** Can be focused on any domain — market research, competitor analysis, technical surveys, etc.

---

## Hosted Tools

OpenAI provides **3 hosted tools** — tools that run remotely on OpenAI's infrastructure:

| Tool | Purpose |
|---|---|
| **Web Search Tool** | Search the internet on behalf of the agent |
| **File Search Tool** | Search across OpenAI-hosted vector stores |
| **Computer Tool** | Take screenshots, click around a computer |

> This lesson uses the **Web Search Tool**. Computer tool equivalent will be built locally later in the course.

---

## Cost Awareness ⚠️

The OpenAI Web Search Tool is **not free**:

| Context Size | Approximate Cost |
|---|---|
| Low | ~$0.025 per call |
| Medium | slightly more |
| High | significantly more |

A typical deep research run (~10 searches) can cost **$0.25–$1.00+**.

**Tips to manage cost:**
- Use `search_context_size="low"` during development
- Use `model="gpt-4o-mini"` (much cheaper than GPT-4)
- Monitor usage at [platform.openai.com](https://platform.openai.com)
- Check current pricing — it changes and varies by region

---

## The Search Agent

### Instructions (System Prompt)

```
You are a research assistant. Given a search term, you search the web for that term
and produce a concise summary of 2-3 paragraphs. Capture the main points, write
succinctly. No need for perfect grammar — output will be consumed by someone
synthesizing a report.
```

### Implementation

```python
from agents import Agent, WebSearchTool, ModelSettings

search_agent = Agent(
    name="Search Agent",
    instructions=search_instructions,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required")  # forces tool use
)
```

**Key parameters:**

| Parameter | Purpose |
|---|---|
| `WebSearchTool(search_context_size="low")` | Hosted web search, lowest cost tier |
| `model="gpt-4o-mini"` | Cheapest model option |
| `ModelSettings(tool_choice="required")` | Forces the agent to always use the tool — no discretion |

---

## Running the Search Agent

```python
result = await Runner.run(search_agent, "Latest AI agent frameworks in 2025")
print(result.final_output)
```

Returns a markdown-formatted summary of web search results.

---

## Key Takeaways

- **Hosted tools** offload execution to OpenAI's infrastructure — no local setup needed
- `tool_choice="required"` via `ModelSettings` makes tool use mandatory for the agent
- The search agent is the first building block — deeper orchestration comes next
- Always use traces to inspect what the agent searched and what it returned
- Cost management is important — use `low` context size and `gpt-4o-mini` during development

---

## What's Next

Building out the full deep research pipeline:
- A **planner agent** to generate a list of search queries
- A **synthesis agent** to combine search results into a final report
- **Structured outputs** (Pydantic) to enforce report format
- Running searches in **parallel** with `asyncio.gather()`