/**
 * Step 1: Create the agent.
 *
 * In Mastra an agent is an Agent: a name, instructions (its system prompt), and a
 * model. The model here comes from vertex_client.ts, which points the Vercel AI SDK
 * at Vertex AI's OpenAI-compatible endpoint using Application Default Credentials
 * (`gcloud auth application-default login`). Nothing runs yet; we just build it.
 * Run it with: npm run step1
 */

import "./env.ts";
import { Agent } from "@mastra/core/agent";
import { getVertexModel } from "./vertex_client.ts";

const agent = new Agent({
  id: "assistant",
  name: "Assistant",
  instructions: "You are a concise, friendly assistant. Reply in a single short sentence.",
  model: await getVertexModel(),
});

console.log(`Created agent: ${agent.name}`);
