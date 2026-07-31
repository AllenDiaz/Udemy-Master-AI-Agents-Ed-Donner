/**
 * Vertex AI wiring for the Mastra worker.
 *
 * Every Mastra agent this week reaches its model through the Vercel AI SDK.
 * Vertex AI serves an OpenAI-compatible Chat Completions endpoint, so
 * `createOpenAI` from `@ai-sdk/openai` works against it once we point it at
 * Vertex's base URL and hand it a fresh OAuth token as the API key. This
 * module is the one place that knows either value.
 *
 * Docs:
 * - https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/call-gemini-using-openai-library
 *
 * Env vars:
 * - GOOGLE_CLOUD_PROJECT   (required) the GCP project with Vertex AI enabled
 * - GOOGLE_CLOUD_LOCATION  (optional, default "global") the Vertex region
 * - VERTEX_DEFAULT_MODEL   (optional, default "gemini-2.5-flash") fallback id
 *
 * Auth uses Application Default Credentials via google-auth-library. Run
 * `gcloud auth application-default login` once, then rebuild the client each
 * time you want a fresh token (they expire after ~1 hour).
 */

import { GoogleAuth } from "google-auth-library";
import { createOpenAI } from "@ai-sdk/openai";

export const DEFAULT_MODEL = "gemini-2.5-flash";
export const DEFAULT_LOCATION = "global";

/** Return the OpenAI-compatible base URL for this project + location. */
export function getBaseUrl(): string {
  const project = process.env.GOOGLE_CLOUD_PROJECT;
  if (!project) {
    throw new Error(
      "GOOGLE_CLOUD_PROJECT is not set. Copy 5_agent_frameworks/.env.example to .env and fill in your GCP project id.",
    );
  }
  const location = process.env.GOOGLE_CLOUD_LOCATION ?? DEFAULT_LOCATION;
  const host = location === "global" ? "aiplatform.googleapis.com" : `${location}-aiplatform.googleapis.com`;
  return `https://${host}/v1beta1/projects/${project}/locations/${location}/endpoints/openapi`;
}

/** Return a fresh Vertex AI OAuth token via Application Default Credentials. */
export async function getAccessToken(): Promise<string> {
  const auth = new GoogleAuth({ scopes: ["https://www.googleapis.com/auth/cloud-platform"] });
  const client = await auth.getClient();
  const { token } = await client.getAccessToken();
  if (!token) {
    throw new Error(
      "Failed to obtain a Vertex AI access token via ADC. Run `gcloud auth application-default login` and try again.",
    );
  }
  return token;
}

/** Prepend the "google/" prefix Vertex's OpenAI-compat endpoint expects. */
export function resolveModel(model?: string | null): string {
  const name = model ?? process.env.VERTEX_DEFAULT_MODEL ?? DEFAULT_MODEL;
  return name.includes("/") ? name : `google/${name}`;
}

/**
 * Build a Vercel AI SDK provider pointed at Vertex AI, and return the model
 * instance for the given id. `await getVertexModel()` is the shape Mastra's
 * `model` field wants.
 */
export async function getVertexModel(model?: string | null) {
  const provider = createOpenAI({
    baseURL: getBaseUrl(),
    apiKey: await getAccessToken(),
  });
  return provider(resolveModel(model));
}
