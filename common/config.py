"""
Shared configuration loader for AWS Strands Agents Masterclass.

Reads `settings.config` from the repository root and returns a configured
Strands model instance (BedrockModel, OpenAIModel, or OllamaModel).
"""

import os
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SETTINGS_PATH = REPO_ROOT / "settings.config"


def load_settings(path: Path = SETTINGS_PATH) -> dict[str, str]:
    """Parse KEY='value' lines from settings.config into a dictionary."""
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    pattern = r"^[ \t]*(\w+)[ \t]*=[ \t]*['\"]?(.*?)['\"]?[ \t]*$"
    return dict(re.findall(pattern, text, re.M))


def get_model() -> Any:
    """Return a Strands Model object based on settings.config or environment variables."""
    cfg = load_settings()

    nvidia_key = cfg.get("NVIDIA_API_KEY") or os.getenv("NVIDIA_API_KEY")
    if nvidia_key:
        from strands.models.openai import OpenAIModel

        return OpenAIModel(
            client_args={
                "api_key": nvidia_key,
                "base_url": "https://integrate.api.nvidia.com/v1",
            },
            model_id=cfg.get("NVIDIA_MODEL", "nvidia/nemotron-3-super-120b-a12b"),
        )

    openai_key = cfg.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if openai_key:
        from strands.models.openai import OpenAIModel

        return OpenAIModel(
            client_args={"api_key": openai_key},
            model_id=cfg.get("OPENAI_MODEL", "gpt-4o-mini"),
        )

    ollama_model = cfg.get("OLLAMA_MODEL") or os.getenv("OLLAMA_MODEL")
    if ollama_model:
        from strands.models.ollama import OllamaModel

        return OllamaModel(
            host=cfg.get("OLLAMA_HOST", "http://localhost:11434"),
            model_id=ollama_model,
        )

    from strands.models.bedrock import BedrockModel

    return BedrockModel(
        model_id=cfg.get("BEDROCK_MODEL_ID", "us.amazon.nova-pro-v1:0"),
        region_name=cfg.get("AWS_REGION", os.getenv("AWS_REGION", "us-east-1")),
    )

