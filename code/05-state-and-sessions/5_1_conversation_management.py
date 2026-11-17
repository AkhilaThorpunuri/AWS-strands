"""
5.1 Conversation Management
Module 5 · State, Sessions & Memory | Read first: md/05-state-and-sessions/5_1_conversation_management.md

What you'll learn:
  - How multi-turn memory works in agent.messages.
  - How SlidingWindowConversationManager caps context size automatically.

Run (from the repo root):
  .venv\\Scripts\\python code\\05-state-and-sessions\\5_1_conversation_management.py
"""

import io
import sys
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager
from common.config import get_model

conversation_manager = SlidingWindowConversationManager(window_size=4)

agent = Agent(
    model=get_model(),
    conversation_manager=conversation_manager,
    system_prompt="Be concise (1 sentence).",
    callback_handler=None,
)

print("Turn 1:", agent("Hi, my name is Akhila and I build agents on AWS."))
print("Turn 2:", agent("What am I building and on which cloud?"))
print("Turn 3:", agent("Give me one tip for keeping agent prompts short."))
print(f"\nMessages stored (window_size=4): {len(agent.messages)}")

# ---------------------------------------------------------------
# Takeaways
#   - agent.messages holds the active conversation history.
#   - SlidingWindowConversationManager prevents unbounded token growth.
# ---------------------------------------------------------------

