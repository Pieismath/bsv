"""Analyze a reference shot via Claude vision and return structured JSON."""

import base64
import json
import os
import re
from pathlib import Path

import anthropic
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=True)

MODEL = os.environ.get("SHOT_ANALYZER_MODEL", "claude-opus-4-7")
MAX_TOKENS = int(os.environ.get("SHOT_ANALYZER_MAX_TOKENS", "4096"))

PROMPT_PATH = PROJECT_ROOT / "prompts" / "shot_analyzer.md"

MEDIA_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
}


def load_prompt() -> str:
    return PROMPT_PATH.read_text()


def encode_image(image_path: str) -> tuple[str, str]:
    path = Path(image_path)
    media_type = MEDIA_TYPES.get(path.suffix.lower())
    if media_type is None:
        raise ValueError(
            f"Unsupported image extension: {path.suffix}. "
            f"Supported: {sorted(MEDIA_TYPES.keys())}"
        )
    data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")
    return media_type, data


def strip_fences(text: str) -> str:
    text = text.strip()
    fence_pattern = r"^```(?:json)?\s*\n?(.*?)\n?```\s*$"
    match = re.match(fence_pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text


def analyze(image_path: str) -> dict:
    prompt = load_prompt()
    media_type, image_data = encode_image(image_path)

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
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
