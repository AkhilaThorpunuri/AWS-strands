"""
8.1 AWS Lambda & API Gateway
Module 8 · Production & AWS Deployment | Read first: md/08-production-and-deployment/8_1_aws_lambda_deployment.md

What you'll learn:
  - How to structure a Strands agent for AWS Lambda and simulate an API Gateway event locally.

Run (from the repo root):
  .venv\\Scripts\\python code\\08-production-and-deployment\\8_1_lambda_handler.py
"""

import json
import io
import sys
from pathlib import Path
from typing import Any

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent
from strands.vended_tools import http_request
from common.config import get_model

# Initialize model at module scope so warm Lambda invocations reuse it
MODEL = get_model()


def lambda_handler(event: dict[str, Any], context: Any = None) -> dict[str, Any]:
    """AWS Lambda entry point compatible with API Gateway proxy events."""
    body = event.get("body") or "{}"
    payload = json.loads(body) if isinstance(body, str) else body

    prompt = payload.get("prompt", "Hello!")
    session_id = payload.get("session_id", "default")

    agent = Agent(
        model=MODEL,
        tools=[http_request],
        system_prompt="You are a concise cloud assistant.",
        callback_handler=None,
    )
    answer = str(agent(prompt))

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"session_id": session_id, "answer": answer}),
    }


if __name__ == "__main__":
    sample_event = {"body": json.dumps({"session_id": "req-101", "prompt": "What is Amazon S3 in 1 sentence?"})}
    response = lambda_handler(sample_event)
    print("Simulated API Gateway Response:")
    print(f"Status: {response['statusCode']}")
    print(f"Body: {response['body']}")

# ---------------------------------------------------------------
# Takeaways
#   - Keep model initialization outside lambda_handler for warm-start speed.
# ---------------------------------------------------------------

