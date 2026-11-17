"""
3.3 Model Context Protocol (MCP)
Module 3 · Tools & MCP | Read first: md/03-tools-and-mcp/3_3_mcp_tools.md

What you'll learn:
  - How to connect a Strands Agent to an MCP server using MCPClient over stdio.
  - Uses a tiny inline Python MCP server so the script runs self-contained.

Run (from the repo root):
  .venv\\Scripts\\python code\\03-tools-and-mcp\\3_3_mcp_tools.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.tools.mcp import MCPClient
from common.config import get_model

# Minimal inline MCP server script launched via `python -c`
INLINE_MCP_SERVER = """
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("demo-tools")

@mcp.tool()
def word_count(text: str) -> int:
    \"\"\"Count the number of words in a string.\"\"\"
    return len(text.split())

mcp.run(transport="stdio")
"""

mcp_client = MCPClient(
    lambda: stdio_client(  # type: ignore[arg-type]
        StdioServerParameters(command=sys.executable, args=["-c", INLINE_MCP_SERVER])
    )
)

with mcp_client:
    tools = mcp_client.list_tools_sync()
    print("Discovered MCP tools:", [t.tool_name for t in tools])

    agent = Agent(model=get_model(), tools=tools)
    result = agent("Use word_count to count words in: 'Strands makes MCP integration effortless'.")
    print(f"\nResponse:\n{result}")

# ---------------------------------------------------------------
# Takeaways
#   - MCPClient wraps stdio, SSE, or Streamable HTTP MCP servers.
#   - Keep agent execution inside `with mcp_client:` so the connection stays alive.
# ---------------------------------------------------------------

