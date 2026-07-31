# Swapping the models

The agent loop uses two models: one for the Google ADK orchestrator agent, which
leads the team, authors the look and the hub, and plays the games to check them,
and one shared by the five workers that build the games. Every worker in this
week now runs on **Google Vertex AI Gemini**; the orchestrator does too, through
ADK's native Vertex backend. Both defaults are set in one place, `config.py`:

```python
ORCHESTRATOR_MODEL = os.environ.get("ORCHESTRATOR_MODEL", "gemini-2.5-flash")  # bigger: gemini-2.5-pro
WORKER_MODEL = os.environ.get("WORKER_MODEL", "gemini-2.5-flash")  # bigger: gemini-2.5-pro
```

Both values are plain Gemini ids (no `google/` prefix — each worker's own
`vertex_client.py` adds that when it needs to). Any Vertex-served id works. To
run bigger, change the two strings, or override either for a single run:

```bash
ORCHESTRATOR_MODEL=gemini-2.5-pro WORKER_MODEL=gemini-2.5-pro uv run agent_loop.py
```

Auth is Application Default Credentials, once per machine:

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable aiplatform.googleapis.com --project YOUR_PROJECT_ID
```

Then set `GOOGLE_CLOUD_PROJECT` (and optionally `GOOGLE_CLOUD_LOCATION`) in your
`.env` — see `../.env.example`. The orchestrator passes `WORKER_MODEL` to each
worker through the environment, so every worker uses the model you choose here.
Run a worker on its own (the Day 2 to 4 demo, with no arguments) and it falls
back to its own committed default, so the standalone days are unaffected.

A worker speaks to whichever provider its framework points at. The workers here
now use Vertex AI's OpenAI-compat endpoint. To point one at a different
provider, change the model client inside that worker exactly as its own day's
`SWAP_AI` notes describe; the orchestrator does not need to know.

## The browser the QA agent uses

The check-the-work step is itself an agent. To judge a game, the orchestrator hands it to a short-lived QA agent that plays it in a browser. That browser comes through the Playwright MCP server, launched on demand with `npx @playwright/mcp` (no install step, like the filesystem MCP server you have used all week) and driving your system Google Chrome. A fresh QA agent per game keeps each browser session small and focused.

By default that Chrome window is visible so you can watch the agent play each game. Set `QA_HEADLESS=1` to run the checks without a window, which is handy on a headless or CI machine.

If Chrome or the MCP server is unavailable, the run still completes: `test_game` reports back that it could not reach the browser, the orchestrator moves on, and the finished site still opens for you to play.
