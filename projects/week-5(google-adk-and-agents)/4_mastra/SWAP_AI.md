# Pointing this day at a different model

Mastra resolves models through the Vercel AI SDK. Every script in this day now
defaults to **Google Vertex AI Gemini** via Vertex's OpenAI-compatible Chat
Completions endpoint. The wiring — base URL, ADC access token (via
`google-auth-library`), and the `google/` prefix Vertex wants — lives in one
place, `vertex_client.ts`, which every script imports:

```typescript
import { getVertexModel } from "./vertex_client.ts";

const worker = new Agent({
  name: "Worker",
  instructions: INSTRUCTIONS,
  model: await getVertexModel(),           // or await getVertexModel(process.env.WORKER_MODEL)
  tools: { ...boardTools, ...(await filesystem.listTools()) },
});
```

Auth is Application Default Credentials. Once, per machine:

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable aiplatform.googleapis.com --project YOUR_PROJECT_ID
```

Then set `GOOGLE_CLOUD_PROJECT` (and optionally `GOOGLE_CLOUD_LOCATION`) in your
`.env` — see `../.env.example`. The worker also reads `WORKER_MODEL` for the
Gemini id, so `WORKER_MODEL=gemini-2.5-pro npm run worker` picks a bigger model
for a single run.

## Swapping to OpenAI or another OpenAI-compatible endpoint

The Vercel AI SDK also ships a shorthand model-routing string, `"provider/model"`,
which reads `OPENAI_API_KEY` from `.env` and calls OpenAI directly. To reach
OpenAI, drop the `getVertexModel` call and pass the string:

```typescript
const worker = new Agent({
  name: "Worker",
  instructions: INSTRUCTIONS,
  model: "openai/gpt-4o-mini",
  tools: { ...boardTools, ...(await filesystem.listTools()) },
});
```

For a custom endpoint such as OpenRouter, build a provider with a `baseURL` and
use it in place of the routing string:

```typescript
import { createOpenAI } from "@ai-sdk/openai";

const provider = createOpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: process.env.OPENROUTER_API_KEY,
});

const worker = new Agent({
  name: "Worker",
  instructions: INSTRUCTIONS,
  model: provider("gpt-4o-mini"),
  tools: { ...boardTools, ...(await filesystem.listTools()) },
});
```

For an endpoint that only mimics the chat-completions shape,
`createOpenAICompatible({ baseURL, name, apiKey })` from
`@ai-sdk/openai-compatible` is the leaner alternative, used the same way.

Everything else in the day stays exactly the same. The board tools, the
filesystem MCP server, and the board are all model-agnostic, so only the one
model line changes.
