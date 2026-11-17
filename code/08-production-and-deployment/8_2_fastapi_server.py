"""
8.2 Containers & FastAPI Serving
Module 8 · Production & AWS Deployment | Read first: md/08-production-and-deployment/8_2_agentcore_and_containers.md

What you'll learn:
  - How to expose a Strands agent via FastAPI with both JSON (/invoke) and SSE (/stream) endpoints.

Run as server:
  .venv\\Scripts\\uvicorn code.08-production-and-deployment.8_2_fastapi_server:app --port 8000
Or run quick smoke test:
  .venv\\Scripts\\python code\\08-production-and-deployment\\8_2_fastapi_server.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from strands import Agent
from common.config import get_model

app = FastAPI(title="Strands Agent Service")
MODEL = get_model()


class PromptRequest(BaseModel):
    prompt: str


@app.post("/invoke")
def invoke_agent(req: PromptRequest) -> dict[str, str]:
    agent = Agent(model=MODEL, system_prompt="Be helpful and concise.", callback_handler=None)
    return {"response": str(agent(req.prompt))}


@app.post("/stream")
async def stream_agent(req: PromptRequest) -> StreamingResponse:
    agent = Agent(model=MODEL, system_prompt="Be helpful and concise.", callback_handler=None)

    async def event_generator():
        async for event in agent.stream_async(req.prompt):
            if "data" in event:
                yield f"data: {event['data']}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    print("Running /invoke handler directly...")
    out = invoke_agent(PromptRequest(prompt="Explain containers on AWS in one sentence."))
    print(out)

# ---------------------------------------------------------------
# Takeaways
#   - FastAPI + stream_async() is ready for Docker, ECS, or Bedrock AgentCore.
# ---------------------------------------------------------------

