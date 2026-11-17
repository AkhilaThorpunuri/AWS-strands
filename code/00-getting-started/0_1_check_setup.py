"""
0.1 Setup & Model Keys
Module 0 · Getting Started | Read first: md/00-getting-started/0_1_setup_and_keys.md

What you'll learn:
  - How scripts in this course load model settings from settings.config
  - How to verify Python, strands-agents, and your model provider all work

Run (from the repo root):
  .venv\\Scripts\\python code\\00-getting-started\\0_1_check_setup.py
"""

import io
import sys
import time
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from common.config import SETTINGS_PATH, get_model


def check(label: str, ok: bool, detail: str) -> bool:
    print(f"  {'✅' if ok else '❌'} {label:<24} {detail}")
    return ok


print("===== SETUP CHECK =====\n")

# 1. Python version check
py_ok = sys.version_info >= (3, 10)
check("Python 3.10+", py_ok, sys.version.split()[0])

# 2. strands-agents installed
try:
    sdk_ver = version("strands-agents")
    sdk_ok = True
except PackageNotFoundError:
    sdk_ver = "not installed (run: pip install -r requirements.txt)"
    sdk_ok = False
check("strands-agents", sdk_ok, sdk_ver)

# 3. settings.config present
cfg_ok = SETTINGS_PATH.exists()
check(
    "settings.config",
    cfg_ok,
    str(SETTINGS_PATH) if cfg_ok else "missing — copy example-settings.config to settings.config",
)

# 4. Live model smoke test
if sdk_ok:
    from strands import Agent

    model = get_model()
    check("Model configured", True, type(model).__name__)
    try:
        t0 = time.perf_counter()
        agent = Agent(model=model, callback_handler=None)
        result = agent("Reply with the single word READY and nothing else.")
        elapsed = time.perf_counter() - t0
        check("Agent responds", True, f"'{str(result).strip()}' in {elapsed:.1f}s")
        print("\nAll good. You're ready for Module 1.")
    except Exception as exc:
        check("Agent responds", False, str(exc))
        print("\nCheck your credentials in settings.config or AWS CLI configuration.")

# ---------------------------------------------------------------
# Takeaways
#   - Credentials live in settings.config, never in source code.
#   - common.config.get_model() lets every script work with Bedrock, OpenAI, or Ollama.
# ---------------------------------------------------------------

