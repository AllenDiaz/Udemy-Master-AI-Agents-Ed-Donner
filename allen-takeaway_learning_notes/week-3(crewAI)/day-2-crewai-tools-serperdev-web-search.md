# CrewAI — Adding Tools (SerperDevTool for Live Web Search)

## Overview

This lesson adds a **real-time web search tool** to the financial researcher crew using CrewAI's built-in `SerperDevTool`. This fixes the knowledge cutoff limitation exposed in the previous run and demonstrates how trivially easy it is to equip a CrewAI agent with tools.

---

## The Problem: Knowledge Cutoff

Running the financial researcher crew without tools produced a report dated **October 2023** — the training cutoff of DeepSeek. Real financial research requires **current data**.

---

## The Fix: SerperDevTool

CrewAI provides built-in tool wrappers. `SerperDevTool` enables Google search via the SerpDev API.

### Prerequisites

Add your SerpDev API key to `.env`:
```bash
SERPER_API_KEY=your_key_here
```

### Adding the Tool in `crew.py`

```python
from crewai_tools import SerperDevTool

@CrewBase
class FinancialResearcherCrew:
    agents_config = "config/agents.yaml"
    tasks_config  = "config/tasks.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            tools=[SerperDevTool()],   # ← one line to add the tool
            verbose=True
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(config=self.agents_config["analyst"], verbose=True)
```

> Only the `researcher` agent gets the search tool — the `analyst` synthesizes from context, no search needed.

That's it. One import, one line. CrewAI handles the rest.

---

## Results Comparison

| | Without Tool | With Tool |
|---|---|---|
| Data recency | October 2023 (training cutoff) | Early 2025 (live search) |
| Search calls | None | Multiple (Tesla latest news, financials, etc.) |
| Cost | Free | Free (SerpDev credits) |
| Output quality | Good but stale | Current and accurate |

---

## Cost Advantage Over OpenAI Hosted Search

| Tool | Cost per search |
|---|---|
| OpenAI WebSearchTool | ~$0.025 |
| SerperDevTool | Free (2,500 credits included) |

---

## Key Takeaways

- Adding a tool to a CrewAI agent is a **one-liner**: `tools=[SerperDevTool()]`
- Assign tools **only to agents that need them** — the analyst gets context from the researcher, not direct search access
- `SerperDevTool` is a built-in CrewAI tool — no custom JSON schema required
- Live search completely resolves the knowledge cutoff problem for research tasks
- The full pipeline (search → synthesize → report) produces genuinely useful, professional output in seconds

---

## Final Financial Researcher Crew — Complete Picture

```
main.py → kickoff(inputs={"company": "Tesla"})
    │
    ▼
[research_task] → researcher (GPT-4o-mini + SerperDevTool)
                  → searches Google for current Tesla news/financials
    │
    ▼  (output passed via context)
[analysis_task] → analyst (Groq/Llama) → synthesizes into report → outputs/report.md
```

---

## Related Concepts

- Other built-in CrewAI tools: `FileReadTool`, `CSVSearchTool`, `WebsiteSearchTool`
- Custom tool creation in CrewAI (`tools/` directory)
- `context` in `tasks.yaml` for passing outputs between tasks
- SerpDev API (`serper.dev`)