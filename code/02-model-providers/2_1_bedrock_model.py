"""
2.1 Amazon Bedrock
Module 2 · Model Providers | Read first: md/02-model-providers/2_1_bedrock_model.md

What you'll learn:
  - How to configure BedrockModel explicitly with model_id, region_name, temperature, and streaming.

Run (from the repo root):
  .venv\\Scripts\\python code\\02-model-providers\\2_1_bedrock_model.py
"""

import os
import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent
from strands.models.bedrock import BedrockModel
from common.config import load_settings

cfg = load_settings()
model_id = cfg.get("BEDROCK_MODEL_ID", "us.amazon.nova-pro-v1:0")
region = cfg.get("AWS_REGION", os.getenv("AWS_REGION", "us-east-1"))

bedrock_model = BedrockModel(
    model_id=model_id,
    region_name=region,
    temperature=0.3,
    streaming=True,
)

print(f"Using BedrockModel: {model_id} in {region}\n")
agent = Agent(model=bedrock_model, system_prompt="Answer in two concise sentences.")
print(agent("What is Amazon Bedrock and why use it with Strands?"))

# ---------------------------------------------------------------
# Takeaways
#   - BedrockModel uses boto3 / IAM credentials automatically.
#   - Prefer cross-region inference profile IDs (us.*, eu.*) for higher throughput.
# ---------------------------------------------------------------

