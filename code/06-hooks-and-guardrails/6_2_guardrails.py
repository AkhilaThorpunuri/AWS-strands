"""
6.2 Bedrock Guardrails & Safety
Module 6 · Hooks, Guardrails & Observability | Read first: md/06-hooks-and-guardrails/6_2_guardrails.md

What you'll learn:
  - How to wire Amazon Bedrock Guardrails into BedrockModel (when configured).
  - How to enforce deterministic output safety checks in Python for any provider.

Run (from the repo root):
  .venv\\Scripts\\python code\\06-hooks-and-guardrails\\6_2_guardrails.py
"""

import re
import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent
from common.config import get_model, load_settings

cfg = load_settings()

# Optional: if you have a Bedrock Guardrail, configure it in settings.config
guardrail_id = cfg.get("BEDROCK_GUARDRAIL_ID")
if guardrail_id:
    from strands.models.bedrock import BedrockModel

    model = BedrockModel(
        model_id=cfg.get("BEDROCK_MODEL_ID", "us.amazon.nova-pro-v1:0"),
        region_name=cfg.get("AWS_REGION", "us-east-1"),
        guardrail_id=guardrail_id,
        guardrail_version=cfg.get("BEDROCK_GUARDRAIL_VERSION", "DRAFT"),
    )
else:
    model = get_model()


def enforce_safe_output(text: str) -> str:
    """Deterministic post-check that redacts SSN-like patterns or emails."""
    if re.search(r"\b\d{3}-\d{2}-\d{4}\b", text) or re.search(r"\S+@\S+\.\S+", text):
        return "[BLOCKED] Response contained sensitive PII and was redacted."
    return text


agent = Agent(
    model=model,
    system_prompt="Answer concisely. Never include personal emails or SSNs.",
    callback_handler=None,
)

print("--- Safe prompt ---")
print(enforce_safe_output(str(agent("What is Amazon S3 in one sentence?"))))

print("\n--- Deterministic PII check ---")
sample_leaky = "Contact jane.doe@example.com or SSN 123-45-6789."
print(enforce_safe_output(sample_leaky))

# ---------------------------------------------------------------
# Takeaways
#   - BedrockModel natively supports guardrail_id + guardrail_version.
#   - Deterministic Python checks guarantee hard policy enforcement on any model.
# ---------------------------------------------------------------

