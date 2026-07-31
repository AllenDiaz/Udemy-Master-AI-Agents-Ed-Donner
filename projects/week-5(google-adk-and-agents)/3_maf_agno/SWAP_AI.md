# Pointing this day at a different model

Both workers here (`maf_worker.py` and `agno_worker.py`) now default to **Google
Vertex AI Gemini** via Vertex's OpenAI-compatible Chat Completions endpoint.
The wiring — base URL, ADC access token, and the `google/` prefix Vertex wants
on model ids — lives in one place, `vertex_client.py`, which both workers
import. Auth is Application Default Credentials; once, per machine:

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable aiplatform.googleapis.com --project YOUR_PROJECT_ID
```

Then set `GOOGLE_CLOUD_PROJECT` (and optionally `GOOGLE_CLOUD_LOCATION`) in your
`.env` — see `../.env.example`. Both workers read `WORKER_MODEL` for the Gemini
id, so the quickest swap between Gemini models is `WORKER_MODEL=gemini-2.5-pro
uv run maf_worker.py`.

## Swapping to OpenAI or another OpenAI-compatible endpoint

Each framework reaches its model in one place; change it in whichever worker
you are running.

### Microsoft Agent Framework

MAF reaches the model through a chat client, and this day uses `OpenAIChatClient`.
Drop the `vertex_client` bits and let it read `OPENAI_API_KEY` from the env, or
point it at any other endpoint:

```python
from agent_framework.openai import OpenAIChatClient

client = OpenAIChatClient(
    model="gpt-4o-mini",
    # base_url="https://openrouter.ai/api/v1",       # for a custom endpoint
    # api_key=os.environ["OPENROUTER_API_KEY"],
)
```

With no `base_url`, the client reads `OPENAI_API_KEY` and calls OpenAI directly.
Nothing else in `maf_worker.py` changes.

### Agno

Agno calls OpenAI through `OpenAIChat`; for any other OpenAI-compatible
endpoint it ships `OpenAILike`, which takes the same `id` plus a `base_url` and
`api_key`. `agno_worker.py` already uses `OpenAILike` (for the Vertex swap), so
pointing it elsewhere is a two-line change:

```python
from agno.models.openai.like import OpenAILike

model = OpenAILike(
    id="gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
```

To go back to plain OpenAI, `from agno.models.openai import OpenAIChat` and
`model = OpenAIChat(id="gpt-4o-mini")` is the more idiomatic form.

Everything else in the day stays exactly the same. The board tools, the
filesystem MCP server, and the board are all model-agnostic, so only the model
wiring changes.
