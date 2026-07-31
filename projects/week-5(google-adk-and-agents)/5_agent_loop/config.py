"""The two models the agent loop uses, kept in one place so they are easy to swap.

Every worker in this week now runs on Google Vertex AI Gemini. The orchestrator
(Google ADK) uses ADK's native Vertex backend; the five workers use Vertex's
OpenAI-compatible endpoint through their own framework's model client. Both
values are Gemini model ids (bare, no ``google/`` prefix — the worker helpers
add that themselves when they need to).

Override either one for a single run without editing the file:

    ORCHESTRATOR_MODEL=gemini-2.5-pro WORKER_MODEL=gemini-2.5-flash uv run agent_loop.py
"""

import os

ORCHESTRATOR_MODEL = os.environ.get("ORCHESTRATOR_MODEL", "gemini-2.5-flash")  # bigger: gemini-2.5-pro
WORKER_MODEL = os.environ.get("WORKER_MODEL", "gemini-2.5-flash")  # bigger: gemini-2.5-pro
