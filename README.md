# Master AI Agents — Ed Donner (Udemy)

My hands-on work, labs, and study notes from Ed Donner's **Master AI Agents** course on Udemy.

The course is a 4-week tour of the modern agentic landscape — building agents from scratch, then with the major frameworks (OpenAI Agents SDK, CrewAI, LangGraph/LangChain). This repo contains the lab code I built along the way plus my own lesson-by-lesson summaries.

> **Status: Course complete** — all 4 weeks finished, including the capstone Sidekick project.

> **Note:** The course is taught against the OpenAI API. I've adapted the projects to run on **Google Cloud Vertex AI** (see [Configuration](#configuration)).

---

## Repository Structure

```
.
├── projects/                       # Lab code, organized by week
│   ├── week-1(basic-knowledge-and-setup)/   # Foundations — agents from scratch
│   │   ├── 1_lab1.ipynb            # Agent loop from scratch
│   │   ├── 2_lab2.ipynb            # Tool calling
│   │   ├── 3_lab3.ipynb            # Orchestration patterns
│   │   └── 5_extra.ipynb           # Extra exercises
│   ├── week-2(all-about-openai-agents)/     # OpenAI Agents SDK
│   │   ├── 1_lab1.ipynb            # SDK basics, async Python
│   │   ├── 2_lab2.ipynb            # Handoffs, guardrails
│   │   └── 3_lab3.ipynb            # Deep-research pipeline
│   ├── week-3(crewAI)/             # CrewAI multi-agent projects
│   │   ├── debate/
│   │   ├── financial_researcher/
│   │   ├── stock_picker/
│   │   ├── coder/
│   │   └── engineering_team/
│   └── week-4(langraph-and-langchain)/      # LangGraph / LangChain
│       ├── 1_lab1.ipynb            # State, nodes, edges, reducers, super-steps
│       ├── 2_lab2.ipynb            # Checkpointing, SQLite memory, time travel, tool calling
│       └── 3_lab3.ipynb            # Sidekick capstone (Playwright, 41 tools, evaluator loop, Gradio UI)
│
├── allen-takeaway_learning_notes/  # My personal lesson summaries (markdown), by week/day
│   ├── week-1(basic-knowledge-and-setup)/   # 7 notes
│   ├── week-2(all-about-openai-agents)/     # 8 notes
│   ├── week-3(crewAI)/                      # 13 notes
│   └── week-4(Langraph-and-Langchain)/      # 17 notes
│
├── important/                      # Helper how-tos (e.g. running CrewAI without uv)
├── requirements.txt                # Pinned Python dependencies
└── README.md
```

---

## Course Outline

### Week 1 — Foundations & Setup
Understanding agents vs. workflows, agentic architectures, design patterns, the LLM agent loop, and orchestration — built from scratch in Jupyter notebooks. Covers the core agent loop, tool calling mechanics, evaluator/optimizer workflows, and a survey of agentic frameworks.

### Week 2 — OpenAI Agents SDK
The OpenAI Agents SDK: async Python, agents-as-tools, handoffs, guardrails, and a full **deep-research** pipeline (planner agent, hosted search tools, structured outputs, orchestration).

### Week 3 — CrewAI
Multi-agent crews built with CrewAI. Each subfolder is a self-contained project:

| Project | What it does |
|---|---|
| `debate` | Two agents argue opposing sides; a third decides |
| `financial_researcher` | Researches a company and writes a report (web search via SerperDev) |
| `stock_picker` | Hierarchical crew with memory that picks a stock; structured outputs |
| `coder` | Agent that writes and executes code in a Docker sandbox |
| `engineering_team` | A simulated engineering team (designer, backend, frontend, QA) building a trading platform |

### Week 4 — LangGraph & LangChain
Three labs building toward the capstone:

| Lab | What it covers |
|---|---|
| `1_lab1.ipynb` | LangGraph core: `State`, `Annotated` reducers, `StateGraph`, nodes, edges, compile/invoke |
| `2_lab2.ipynb` | Checkpointing with SQLite, persistent memory, time-travel, tool calling with `ToolNode` and conditional edges, LangSmith tracing |
| `3_lab3.ipynb` | **Sidekick** — a multi-agent LangGraph app with 41 tools (Playwright browser, web search, Wikipedia, file system, push notifications, Python REPL), an evaluator loop, human-in-the-loop approval, and a Gradio UI |

---

## Learning Notes

The `allen-takeaway_learning_notes/` folder holds my own summary for each lesson — concepts, code snippets, and key takeaways — organized by week and day (45 notes total). These are my personal study takeaways, not the official course material.

Highlights:
- **Week 1:** agent vs. workflow patterns, agentic architectures, LLM orchestration, evaluator/optimizer loops
- **Week 2:** async Python deep-dive, OpenAI Agents SDK handoffs, guardrails, deep-research pipeline
- **Week 3:** CrewAI YAML-driven agents/tasks, LiteLLM integration, tools (SerperDev), memory types, hierarchical crews, code-execution agents
- **Week 4:** LangGraph state/reducers/super-steps, SQLite checkpointing, time travel, tool calling, Sidekick internals (`tools.py`, `sidekick.py`, `worker`, `evaluator`, `build_graph`, `run`)

---

## Getting Started

### Prerequisites
- Python 3.11+
- Access to an LLM provider (this repo is configured for Google Cloud Vertex AI)
- For Week 3 (CrewAI): optionally [`uv`](https://docs.astral.sh/uv/); see [`important/`](important/) for running without it
- For Week 4 (Sidekick): Playwright browsers (`playwright install`)

### Setup
```bash
# clone, then from the repo root:
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration
Create a `.env` file in the repo root (it is git-ignored). The projects read configuration for Vertex AI:

```dotenv
GCP_PROJECT=your-gcp-project
GCP_REGION=your-region
GCP_LOCATION=your-location
MODEL_NAME=your-model
VERTEXAI_PROJECT=your-gcp-project
VERTEXAI_LOCATION=your-location
CREWAI_DISABLE_TELEMETRY=true
```

Other framework keys (e.g. `SERPER_API_KEY` for web search, `PUSHOVER_*` for push notifications) can be added as needed by individual projects.

---

## Running the Projects

**Notebook weeks (1, 2, 4):** open the `*.ipynb` files in Jupyter / VS Code and run the cells.

**CrewAI projects (week 3):** each project follows the standard CrewAI layout (`src/<project>/`, `config/*.yaml`). With `uv`:
```bash
cd "projects/week-3(crewAI)/debate"
crewai run
```
Without `uv`, see [`important/instruction-to-run-crew-without-uv.md`](important/instruction-to-run-crew-without-uv.md):
```bash
python -c "import sys; sys.path.insert(0, 'src'); from debate.main import run; run()"
```

---

## Credits

Course: **Master AI Agents** by [Ed Donner](https://www.udemy.com/) on Udemy. This repo is my personal coursework and notes for learning purposes.
