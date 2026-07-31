# Pointing this day at a different model

Every worker in this week now runs on **Google Vertex AI Gemini** by default.
This one is the Google ADK worker, and ADK talks to Gemini natively. Vertex is
selected with two environment settings (both defaulted in `task_worker/agent.py`
and the two A2A demo files, so a plain `uv run worker.py` just works once your
Google Cloud setup is in place):

```python
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "TRUE")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
```

Auth is Application Default Credentials. Once, per machine:

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable aiplatform.googleapis.com --project YOUR_PROJECT_ID
```

Then set `GOOGLE_CLOUD_PROJECT` in your `.env` (see `../.env.example`). The
model is a plain Gemini id — no `google/` prefix, no LiteLLM wrapper — and any
Vertex-served id works: `gemini-2.5-flash`, `gemini-2.5-pro`, and so on. Pick
one for a single run with `WORKER_MODEL=gemini-2.5-pro uv run worker.py`.

## Swapping to any OpenAI-compatible endpoint

To run against OpenAI (or OpenRouter, or a local server), ADK routes through
LiteLLM.

Install the extra in this folder:

```bash
uv add "google-adk[extensions]"
```

Then wrap the model. In `task_worker/agent.py`, swap the model string for a
`LiteLlm` instance and turn off Vertex:

```python
from google.adk.models.lite_llm import LiteLlm

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

root_agent = LlmAgent(
    model=LiteLlm(model="openai/gpt-4o-mini"),   # any LiteLLM model string
    name="task_worker",
    description="Works one task from the SQLite board using its files.",
    instruction=...,        # unchanged
    tools=[show_todos, plan_steps, complete_task, filesystem],
)
```

The `openai/` prefix tells LiteLLM to use the OpenAI chat protocol. With `OPENAI_API_KEY` in your `.env`, `openai/gpt-4o-mini` works with no further configuration.

For a custom endpoint such as OpenRouter, pass `api_base` and `api_key`:

```python
import os

model = LiteLlm(
    model="openai/gpt-4o-mini",
    api_base="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
```

Everything else in the day stays exactly the same. The tools, the filesystem MCP server, and the board are all model-agnostic, so only the one model line changes.
