"""Reason about whether and how Beeble fits a given shot analysis."""

import json
import os
import re
from pathlib import Path

import anthropic
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=True)

MODEL = os.environ.get("BEEBLE_FIT_MODEL", "claude-opus-4-7")
MAX_TOKENS = int(os.environ.get("BEEBLE_FIT_MAX_TOKENS", "4096"))

PROMPT_PATH = PROJECT_ROOT / "prompts" / "beeble_fit.md"


def load_prompt() -> str:
    return PROMPT_PATH.read_text()


def strip_fences(text: str) -> str:
    text = text.strip()
    fence_pattern = r"^```(?:json)?\s*\n?(.*?)\n?```\s*$"
    match = re.match(fence_pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text


def reason_beeble_fit(
    shot_analysis: dict,
    capabilities_doc_path: str = "references/beeble_capabilities.md",
) -> dict:
    prompt = load_prompt()

    caps_path = Path(capabilities_doc_path)
    if not caps_path.is_absolute():
        caps_path = PROJECT_ROOT / capabilities_doc_path
    capabilities_text = caps_path.read_text()

    user_message = (
        f"{prompt}\n\n"
        f"---\n\n"
        f"## Beeble Capabilities Reference (source of truth)\n\n"
        f"{capabilities_text}\n\n"
        f"---\n\n"
        f"## Shot Analysis (input to reason about)\n\n"
        f"```json\n{json.dumps(shot_analysis, indent=2)}\n```\n\n"
        f"Now produce the JSON output per the schema. Return ONLY the JSON."
    )

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": user_message}],
    )

    raw_output = response.content[0].text
    cleaned = strip_fences(raw_output)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        return {
            "error": f"JSON parse failed: {e}",
            "raw_output": raw_output,
            "model": MODEL,
        }
