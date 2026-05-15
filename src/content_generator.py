"""Generate multi-format content from a shot analysis and Beeble fit recipe."""

import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import anthropic
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=True)

MODEL = os.environ.get("CONTENT_GENERATOR_MODEL", "claude-sonnet-4-6")
MAX_TOKENS = int(os.environ.get("CONTENT_GENERATOR_MAX_TOKENS", "4096"))

PROMPTS_DIR = PROJECT_ROOT / "prompts"
PROJECT_CONTEXT_PATH = PROJECT_ROOT / "PROJECT_CONTEXT.md"

FORMAT_PROMPTS = {
    "tiktok": "format_tiktok.md",
    "reddit": "format_reddit.md",
    "xthread": "format_xthread.md",
    "youtube": "format_youtube.md",
}


class NotAFitError(Exception):
    pass


def load_prompt(format_name: str) -> str:
    return (PROMPTS_DIR / FORMAT_PROMPTS[format_name]).read_text()


def load_voice_rules() -> str:
    text = PROJECT_CONTEXT_PATH.read_text()
    match = re.search(
        r"## Voice and taste guidelines\n(.*?)(?=\n## |\Z)", text, re.DOTALL
    )
    if match:
        return "## Voice and taste guidelines\n" + match.group(1).strip()
    return text


def _build_user_message(
    format_prompt: str, voice_rules: str, analysis: dict, fit: dict
) -> str:
    return (
        f"{format_prompt}\n\n"
        f"---\n\n"
        f"## Voice and Taste Rules (from PROJECT_CONTEXT.md, authoritative)\n\n"
        f"{voice_rules}\n\n"
        f"---\n\n"
        f"## Shot Analysis (upstream input)\n\n"
        f"```json\n{json.dumps(analysis, indent=2)}\n```\n\n"
        f"---\n\n"
        f"## Beeble Fit (workflow and hedges, must be honored)\n\n"
        f"```json\n{json.dumps(fit, indent=2)}\n```\n\n"
        f"---\n\n"
        f"Generate the content in the specified format. Output ONLY the content itself, no commentary, no framing text, no preamble."
    )


def _strip_markdown_fences(text: str) -> str:
    text = text.strip()
    lines = text.split("\n")
    cleaned = [l for l in lines if not l.strip().startswith("```")]
    result = "\n".join(cleaned).strip()
    return re.sub(r"\n{3,}", "\n\n", result)


def _generate_one(
    format_name: str, analysis: dict, fit: dict, voice_rules: str
) -> str:
    prompt = load_prompt(format_name)
    user_message = _build_user_message(prompt, voice_rules, analysis, fit)
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": user_message}],
    )
    return _strip_markdown_fences(response.content[0].text)


def generate_content(
    shot_analysis: dict,
    fit_result: dict,
    formats: list = None,
) -> dict:
    if not fit_result.get("is_fit"):
        raise NotAFitError(
            "Cannot generate content: fit_result.is_fit is False. "
            f"Reason: {fit_result.get('fit_reasoning', '(none)')}"
        )

    if formats is None:
        formats = list(FORMAT_PROMPTS.keys())

    invalid = set(formats) - set(FORMAT_PROMPTS.keys())
    if invalid:
        raise ValueError(
            f"Unknown formats: {sorted(invalid)}. "
            f"Valid: {sorted(FORMAT_PROMPTS.keys())}"
        )

    voice_rules = load_voice_rules()

    results = {}
    with ThreadPoolExecutor(max_workers=len(formats)) as pool:
        future_to_format = {
            pool.submit(
                _generate_one, fmt, shot_analysis, fit_result, voice_rules
            ): fmt
            for fmt in formats
        }
        for future in as_completed(future_to_format):
            fmt = future_to_format[future]
            try:
                results[fmt] = future.result()
            except Exception as e:
                results[fmt] = f"ERROR: {type(e).__name__}: {e}"

    return results
