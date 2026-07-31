"""Vertex AI wiring for the workers in this day.

Every worker on Days 2 and 3 speaks OpenAI Chat Completions to whatever URL its
model client points at. Vertex AI serves an OpenAI-compatible Chat Completions
endpoint, so pointing the same clients at Vertex is a two-value swap: a base URL
built from your Google Cloud project and location, and a short-lived OAuth token
from Application Default Credentials (`gcloud auth application-default login`).
This module is the one place that knows either value.

Docs:
- https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/call-gemini-using-openai-library

Env vars:
- GOOGLE_CLOUD_PROJECT   (required) the GCP project with Vertex AI enabled
- GOOGLE_CLOUD_LOCATION  (optional, default "global") the Vertex region
- VERTEX_DEFAULT_MODEL   (optional, default "gemini-2.5-flash") fallback model id
"""

from __future__ import annotations

import os

DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_LOCATION = "global"


def get_base_url() -> str:
    """Return the OpenAI-compatible base URL for this project + location.

    ``location=global`` uses the multi-region endpoint; any other value uses the
    matching regional endpoint (for example ``us-central1``).
    """
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise RuntimeError(
            "GOOGLE_CLOUD_PROJECT is not set. Copy 5_agent_frameworks/.env.example "
            "to .env and fill in your GCP project id."
        )
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", DEFAULT_LOCATION)
    host = "aiplatform.googleapis.com" if location == "global" else f"{location}-aiplatform.googleapis.com"
    return f"https://{host}/v1beta1/projects/{project}/locations/{location}/endpoints/openapi"


def get_access_token() -> str:
    """Return a fresh Vertex AI OAuth token via Application Default Credentials.

    Tokens are short-lived (~1 hour). Each call refreshes, so rebuilding the
    model client mid-run picks up a fresh token.
    """
    import google.auth  # imported lazily; google-auth ships with google-adk
    import google.auth.transport.requests

    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    creds.refresh(google.auth.transport.requests.Request())
    if not creds.token:
        raise RuntimeError(
            "Failed to obtain a Vertex AI access token via ADC. "
            "Run `gcloud auth application-default login` and try again."
        )
    return creds.token


def resolve_model(model: str | None = None) -> str:
    """Return the model id Vertex expects on its OpenAI-compat endpoint.

    Vertex's OpenAI endpoint wants ids prefixed with ``google/`` (for example
    ``google/gemini-2.5-flash``); this helper adds the prefix if missing so
    callers can hand in a bare Gemini id.
    """
    name = model or os.environ.get("VERTEX_DEFAULT_MODEL", DEFAULT_MODEL)
    return name if "/" in name else f"google/{name}"


__all__ = ["DEFAULT_MODEL", "DEFAULT_LOCATION", "get_base_url", "get_access_token", "resolve_model"]
