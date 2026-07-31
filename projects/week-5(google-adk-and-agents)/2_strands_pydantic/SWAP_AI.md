# Pointing this day at a different model

Both workers here (`strands_worker.py` and `pydantic_worker.py`) now default to
**Google Vertex AI Gemini** via Vertex's OpenAI-compatible Chat Completions
endpoint. The wiring — base URL, ADC access token, and the `google/` prefix
Vertex wants on model ids — lives in one place, `vertex_client.py`, which both
workers import. Auth is Application Default Credentials; once, per machine:

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable aiplatform.googleapis.com --project YOUR_PROJECT_ID
```

Then set `GOOGLE_CLOUD_PROJECT` (and optionally `GOOGLE_CLOUD_LOCATION`) in your
`.env` — see `../.env.example`. Both workers read `WORKER_MODEL` for the Gemini
id, so the quickest swap between Gemini models is `WORKER_MODEL=gemini-2.5-pro
uv run strands_worker.py`. Any Vertex-served id works.

## Swapping to OpenAI or another OpenAI-compatible endpoint

Each framework reaches its model in one place; change it in whichever worker
you are running.

### Strands

Strands talks to several providers through dedicated model classes, and this
day uses `OpenAIModel`. Drop the `vertex_client` bits and rebuild the model
around whichever endpoint you want:

```python
from strands.models.openai import OpenAIModel

model = OpenAIModel(
    client_args={
        "api_key": os.environ["OPENAI_API_KEY"],     # or OPENROUTER_API_KEY, etc.
        # "base_url": "https://openrouter.ai/api/v1", # for a custom endpoint
    },
    model_id="gpt-4o-mini",
)
```

With no `base_url`, `OpenAIModel` calls OpenAI directly. Nothing else in
`strands_worker.py` changes.

### Pydantic AI

Pydantic AI picks a provider with a `provider:model` string. The quickest swap
to OpenAI is to hand the agent that string directly:

```python
worker = Agent(f"openai-chat:{MODEL_ID}", instructions=INSTRUCTIONS, ...)
```

For a different endpoint, keep the `OpenAIChatModel` + `OpenAIProvider` shape
that `pydantic_worker.py` already uses and swap in the URL and key:

```python
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

MODEL = OpenAIChatModel(
    "gpt-4o-mini",
    provider=OpenAIProvider(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    ),
)
```

Everything else in the day stays exactly the same. The board tools, the
filesystem MCP server, and the board are all model-agnostic, so only the model
wiring changes.
