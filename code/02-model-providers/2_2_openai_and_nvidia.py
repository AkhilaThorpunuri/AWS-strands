"""
2.2 OpenAI, NVIDIA & Custom Endpoints
Module 2 · Model Providers | Read first: md/02-model-providers/2_2_openai_and_nvidia.md

What you'll learn:
  - How to configure OpenAIModel for OpenAI or any OpenAI-compatible endpoint (e.g. NVIDIA NIM).

Run (from the repo root):
  .venv\\Scripts\\python code\\02-model-providers\\2_2_openai_and_nvidia.py
"""

import os
import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent
from strands.models.openai import OpenAIModel
from common.config import load_settings

cfg = load_settings()
nvidia_key = cfg.get("NVIDIA_API_KEY") or os.getenv("NVIDIA_API_KEY")
openai_key = cfg.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

if nvidia_key:
    model_id = cfg.get("NVIDIA_MODEL", "nvidia/nemotron-3-super-120b-a12b")
    model = OpenAIModel(
        client_args={"api_key": nvidia_key, "base_url": "https://integrate.api.nvidia.com/v1"},
        model_id=model_id,
        params={"temperature": 0.4, "max_tokens": 512},
    )
elif openai_key:
    model_id = cfg.get("OPENAI_MODEL", "gpt-4o-mini")
    model = OpenAIModel(
        client_args={"api_key": openai_key},
        model_id=model_id,
        params={"temperature": 0.4, "max_tokens": 512},
    )
else:
    raise SystemExit("Set NVIDIA_API_KEY or OPENAI_API_KEY in settings.config to run this example.")

print(f"Using OpenAIModel: {model_id}\n")
agent = Agent(model=model, system_prompt="Answer in two concise sentences.")
print(agent("Why is a model-agnostic agent SDK useful?"))

# ---------------------------------------------------------------
# Takeaways
#   - OpenAIModel works with both OpenAI and any OpenAI-compatible base_url.
# ---------------------------------------------------------------

