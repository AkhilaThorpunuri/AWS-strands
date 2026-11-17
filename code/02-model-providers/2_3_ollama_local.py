"""
2.3 Local Models with Ollama
Module 2 · Model Providers | Read first: md/02-model-providers/2_3_ollama_local.md

What you'll learn:
  - How to run a Strands Agent locally using OllamaModel.

Run (from the repo root):
  .venv\\Scripts\\python code\\02-model-providers\\2_3_ollama_local.py
"""

import os
import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent
from strands.models.ollama import OllamaModel
from common.config import load_settings

cfg = load_settings()
host = cfg.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST", "http://localhost:11434"))
model_id = cfg.get("OLLAMA_MODEL", os.getenv("OLLAMA_MODEL", "llama3.2"))

ollama_model = OllamaModel(host=host, model_id=model_id)

print(f"Using OllamaModel: {model_id} at {host}\n")
agent = Agent(model=ollama_model, system_prompt="Answer in two concise sentences.")
print(agent("What are the benefits of running an AI agent locally?"))

# ---------------------------------------------------------------
# Takeaways
#   - OllamaModel runs Strands agents 100% locally with zero API fees.
# ---------------------------------------------------------------

