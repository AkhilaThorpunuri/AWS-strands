"""
5.2 Persistent Sessions
Module 5 · State, Sessions & Memory | Read first: md/05-state-and-sessions/5_2_session_managers.md

What you'll learn:
  - How FileSessionManager persists and restores agent conversations across instances.

Run (from the repo root):
  .venv\\Scripts\\python code\\05-state-and-sessions\\5_2_session_managers.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from common.config import get_model

session_dir = str(REPO_ROOT / ".strands" / "sessions")
session_id = "demo-user-42"

# Run 1: First Agent instance stores a preference
agent_1 = Agent(
    model=get_model(),
    session_manager=FileSessionManager(session_id=session_id, storage_dir=session_dir),
    system_prompt="You remember user preferences concisely.",
    callback_handler=None,
)
print("--- Run 1 (first agent) ---")
print(agent_1("Remember that my preferred AWS region is us-west-2."))

# Run 2: Brand-new Agent instance with the same session_id
agent_2 = Agent(
    model=get_model(),
    session_manager=FileSessionManager(session_id=session_id, storage_dir=session_dir),
    system_prompt="You remember user preferences concisely.",
    callback_handler=None,
)
print("\n--- Run 2 (new Agent instance, same session_id) ---")
print(agent_2("What is my preferred AWS region?"))

# ---------------------------------------------------------------
# Takeaways
#   - FileSessionManager persists messages locally by session_id.
#   - In AWS production, swap to S3SessionManager(session_id=..., bucket=...).
# ---------------------------------------------------------------

