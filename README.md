# Beeble GTM Agent

Prototype shot-breakdown content engine for [Beeble](https://beeble.ai). Takes a reference shot (a film still, a viral commercial moment, a music video frame) and produces channel-specific breakdowns (TikTok script, r/filmmakers post, X thread, YouTube outline) demonstrating how to recreate the shot with Beeble's relighting and background-swap tools. Built for the Basis Set Ventures AI Fellow submission; see [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) for the full brief.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# add your ANTHROPIC_API_KEY to .env
```

`BEEBLE_API_KEY` in `.env.example` is reserved for a future stretch step that calls the SwitchX API. The prototype does not require it.

## Run

```bash
python run.py --shot path/to/image.jpg
```

Outputs land in `outputs/<shot_slug>/`, one file per channel format.

## Layout

```
src/          pipeline steps (shot analyzer, beeble fit, content generator)
prompts/      LLM prompts as .md files, one per pipeline step
references/   beeble_capabilities.md (capability source of truth) and shots/ (input images)
outputs/      generated breakdowns, keyed by shot slug
```
