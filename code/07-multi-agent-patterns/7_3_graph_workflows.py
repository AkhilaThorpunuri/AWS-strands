"""
7.3 Graph Workflows
Module 7 · Multi-Agent Patterns | Read first: md/07-multi-agent-patterns/7_3_graph_workflows.md

What you'll learn:
  - How to build a deterministic multi-agent pipeline with GraphBuilder.

Run (from the repo root):
  .venv\\Scripts\\python code\\07-multi-agent-patterns\\7_3_graph_workflows.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent
from strands.multiagent import GraphBuilder
from common.config import get_model

model = get_model()

researcher = Agent(
    model=model,
    system_prompt="List 3 key technical facts about the given topic in bullet points.",
    callback_handler=None,
)
analyst = Agent(
    model=model,
    system_prompt="Identify the top 2 business benefits from the research provided.",
    callback_handler=None,
)
writer = Agent(
    model=model,
    system_prompt="Write a crisp 3-sentence executive summary combining the facts and benefits.",
    callback_handler=None,
)

builder = GraphBuilder()
builder.add_node(researcher, "researcher")
builder.add_node(analyst, "analyst")
builder.add_node(writer, "writer")
builder.add_edge("researcher", "analyst")
builder.add_edge("analyst", "writer")
builder.set_entry_point("researcher")

graph = builder.build()
result = graph("Serverless AI agents on AWS Lambda")

order = [node.node_id for node in result.execution_order]
print(f"Graph status: {result.status}")
print(f"Execution order: {order}")
print(f"\nFinal report:\n{result.results['writer'].result}")

# ---------------------------------------------------------------
# Takeaways
#   - GraphBuilder enforces deterministic node-to-node execution order.
# ---------------------------------------------------------------

