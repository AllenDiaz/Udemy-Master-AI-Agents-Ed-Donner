# Deep Research — Full Pipeline (Writer, Email & Orchestration)

## Overview

This lesson completes the deep research agent by adding the **writer agent**, **email agent**, and the **orchestration flow** that chains all components together into an end-to-end pipeline: plan → search → write → send.

---

## Full Architecture

```
User Query
    │
    ▼
[Planner Agent]         → outputs WebSearchPlan (3 search items)
    │
    ▼
[Search Agent ×3]       → runs in parallel via asyncio.gather()
    │                     each uses WebSearchTool (hosted)
    ▼
[Writer Agent]          → synthesizes results into ReportData (structured output)
    │
    ▼
[Email Agent]           → formats as HTML, generates subject, sends via SendGrid
```

---

## New Agents

### Writer Agent

Synthesizes all search results into a long-form structured report.

```python
class ReportData(BaseModel):
    short_summary: str
    """A short 2-3 sentence summary of the findings"""

    markdown_report: str
    """The full markdown report — 5 to 10 pages, at least 1000 words"""

    follow_up_suggestions: list[str]
    """Suggested topics to research further"""

writer_agent = Agent(
    name="Writer Agent",
    instructions="""
        You are a senior researcher tasked with writing a cohesive report for a query.
        You'll be provided with the original query and initial research.
        Come up with an outline, then generate the full report.
        Output should be in markdown, lengthy and detailed (5-10 pages, 1000+ words).
    """,
    model="gpt-4o-mini",
    output_type=ReportData   # structured output
)
```

### Email Agent

Converts the markdown report to a formatted HTML email and sends it.

```python
email_agent = Agent(
    name="Email Agent",
    instructions="""
        You are able to send a nicely formatted HTML email based on a detailed report.
        You'll be provided with a report. Use your tool to send one email,
        converting it to clean, well-presented HTML with a subject line.
    """,
    model="gpt-4o-mini",
    tools=[send_email]   # plain function tool via @function_tool decorator
)
```

> The email agent has **full discretion** to write the subject line and reformat the content into HTML — no extra agents needed for this.

---

## The Five Orchestration Functions

### 1. `plan_searches(query)` — Planner

```python
async def plan_searches(query: str) -> WebSearchPlan:
    result = await Runner.run(planner_agent, query)
    print(f"Planning complete: {len(result.final_output.searches)} searches")
    return result.final_output
```

### 2. `perform_searches(search_plan)` — Parallel Search Execution

```python
async def perform_searches(search_plan: WebSearchPlan) -> list[str]:
    tasks = [asyncio.create_task(search(item)) for item in search_plan.searches]
    results = await asyncio.gather(*tasks)
    return results
```

> Uses `asyncio.gather()` to run all searches **in parallel** — significant time saving.

### 3. `search(item)` — Single Search

```python
async def search(item: WebSearchItem) -> str:
    input_text = f"Reason: {item.reason}\nQuery: {item.query}"
    result = await Runner.run(search_agent, input_text)
    return result.final_output
```

> Passes both `reason` and `query` to the search agent — the reason provides context that improves search quality.

### 4. `write_report(query, search_results)` — Synthesis

```python
async def write_report(query: str, search_results: list[str]) -> ReportData:
    input_text = f"Query: {query}\n\nResearch:\n" + "\n\n".join(search_results)
    result = await Runner.run(writer_agent, input_text)
    return result.final_output
```

### 5. `send_report(report)` — Email Delivery

```python
async def send_report(report: ReportData):
    await Runner.run(email_agent, report.markdown_report)
```

---

## Full Orchestration Flow

```python
with trace("Deep Research"):
    print("Starting research...")

    search_plan = await plan_searches(query)
    search_results = await perform_searches(search_plan)
    report = await write_report(query, search_results)
    await send_report(report)

    print("Done! Email sent.")
```

---

## Key Takeaways

- `asyncio.gather()` with `create_task()` runs all searches in parallel — critical for performance
- The `reason` field from `WebSearchItem` is passed into the search agent for better context
- `ReportData` structured output cleanly separates summary, full report, and follow-up suggestions
- The email agent handles HTML formatting and subject generation autonomously — no extra agents needed
- The full pipeline is clean, linear, and easy to extend (swap models, add guardrails, adjust search count)

---

## Cost Summary for Full Run

| Step | Cost Driver | Est. Cost (3 searches) |
|---|---|---|
| Planner | GPT-4o-mini tokens | ~$0.00 |
| Search ×3 | WebSearchTool @ $0.025/call | ~$0.075 |
| Writer | GPT-4o-mini tokens | ~$0.01 |
| Email | GPT-4o-mini tokens | ~$0.01 |
| **Total** | | **~$0.10–$0.20** |

---

## Related Concepts

- `asyncio.create_task()` vs `asyncio.gather()`
- `@function_tool` decorator for plain function tools
- Pydantic structured outputs with field docstrings
- OpenAI Traces for end-to-end pipeline observability