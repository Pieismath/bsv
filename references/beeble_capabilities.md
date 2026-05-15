# Beeble Capabilities Reference

> Living source of truth for what Beeble's products actually do, used by the `beeble_fit` pipeline step to ground recommendations. Source priority: docs.beeble.ai > beeble.ai > PROJECT_CONTEXT.md. No empirical access in prototype phase (no API key), so every claim here is docs-derived. Hedge accordingly in generated outputs.

Last refreshed: 2026-05-15.

---

## SwitchLight 3.0 (powers VFX Pass Generator)

**What it does.** Video-to-PBR model. Converts source footage into a stack of physically-based rendering passes for downstream relighting and compositing in a DCC.

**Output passes.** Source RGB, Normal, BaseColor (albedo), Metallic, Alpha, Depth, Roughness, Specular. Full PBR stack, ready for Nuke, Blender, Unreal, or any DCC that consumes PBR. (Verified at beeble.ai.)

**Product surface.** Exposed as "VFX Pass Generator" inside both Beeble Cloud and Beeble Studio.

**Limits.**
- **Cloud:** up to 2K, max 1 minute per video.
- **Studio (desktop):** up to 4K, max 1 hour per video. Local GPU rendering, no credit cost.

**Stated quality.** Beeble describes the output as "pixel-perfect, production-ready PBR passes" with "state-of-the-art AI rotoscoping with clean, artifact-free mattes." Hedge any specific quality claim in tutorial copy; we have not run it ourselves.

**When to recommend.** When the creator wants to relight a clip cleanly after the fact, integrate AI VFX into a Nuke/Blender pipeline, or extract clean PBR from existing footage for further compositing. The "shoot it flat, light it in post" framing is its natural pitch.

**When not to.** Real-time creative iteration on the look happens in Beeble Editor (fed by the passes), not in the Pass Generator itself.

---

## SwitchX

**What it does.** Video-to-video AI. Swaps environment, lighting, color grade, props, and wardrobe in masked regions of the frame while preserving the subject's identity, motion, and performance in unmasked regions.

**The mask system (this is the UX center).** Four modes documented at docs.beeble.ai:

- **Auto.** AI detects and isolates the main subject automatically. Zero manual input. Best for "I want a clean subject preservation and I'm not picky about exact region edges."
- **Select.** Manual subject selection via SAM3 segmentation. Click to include, right-click to deselect, stack multiple distinct objects as separate selections. Beeble explicitly recommends adding distinct parts as separate objects rather than grouping them. Best for "I want this person and this prop preserved, ignore the rest."
- **Fill.** Selects the entire frame. Keeps geometry and composition, alters only aesthetics. Best for "keep my blocking and framing, just push the look."
- **Upload.** Bring your own alpha matte from external software. Best for pixel-perfect control.

**Reference image.** The visual blueprint. SwitchX extracts style, lighting, color palette, and environment context from the reference and applies them to the source. Beeble: "Your reference image doesn't need to perfectly match your source footage." The reference drives the result more than the prompt does.

**Prompts.** Recommended setting is **Autopilot**, which lets SwitchX engineer the prompt internally from the reference. If overriding, be highly specific (environment, lighting, mood). Vague prompts ("take me to heaven") yield poor results. Beeble explicitly suggests using an LLM to generate detailed prompt variations.

**Camera motion (counter-intuitive constraint).** SwitchX uses the unmasked foreground to infer camera tracking. So:
- **Excels at:** hand-held shots, complex movement, organic camera shake, visible depth changes.
- **Struggles at:** simple linear pans, lateral trucks, locked-off statics where the foreground lacks parallax cues.
- This matters for tutorial framing because the indie creator's instinct is to lock the camera off "to make the AI's job easier." That is the wrong move; a little organic shake helps SwitchX, not hurts it.

**Multi-subject.** Supported via Select mode. Add distinct subjects as separate selections, not as a single grouped mask.

**Output specs.**
- **Resolution:** 720p or 1080p output. Hard cap.
- **Aspect ratio:** always preserved from source.
- **Frame rate:** always preserved from source.
- **Format:** not documented at this fetch.

**Availability.** Cloud-exclusive. Not in Beeble Studio.

**Pro workflow Beeble itself recommends.** Generate an initial reference with an AI image tool, download, refine in Photoshop (color grade, prop adjustments), re-upload for "pixel-perfect results." This is the real cinematographer-grade loop and worth naming in tutorial content because it sounds like work, not magic.

---

## Background Remover

**What it does.** AI-powered alpha extraction. Produces a clean background-free version of the source footage.

**Availability.** Cloud-exclusive.

**Credit cost.** 1 credit per image or per video-second.

**When to recommend.** As a prep step before compositing (e.g., dropping the subject into a new plate in After Effects), or as a keying alternative when no green screen was available on set.

---

## Beeble Studio (Desktop)

**What it is.** Local-only desktop app that runs Beeble's tools on the user's own GPU. Footage never leaves the machine.

**Platforms.** Windows and Linux. (No macOS mentioned in current docs.)

**Includes.** VFX Pass Generator (up to 4K / 1 hour per video, unlimited usage), Beeble Editor.

**Does NOT include.** SwitchX and Background Remover are cloud-exclusive.

**Pricing.** Not on the public pricing page checked on 2026-05-15. PROJECT_CONTEXT.md cites $500/yr indie and $3,000/yr facility; treat as unverified until confirmed at docs.

**Target.** Facilities that need privacy, 4K output, or unlimited rendering. Indie creators with capable GPUs who want to bypass credit caps for high-volume Pass Generator work.

---

## Beeble Cloud (Pricing and Plans)

Verified at beeble.ai/pricing on 2026-05-15.

| Tier | Monthly | Annual | Credits/mo | Notes |
|---|---|---|---|---|
| Starter (Free) | $0 | — | 90 | Non-commercial only. All tools accessible. |
| Creator | $19 | $16 (16% off) | 540 | Commercial use, batch upload, priority support, top-up credits. |
| Professional | $75 | $60 (20% off) | 2,400 | Commercial use, image sequence upload, top-up credits. |

**Credit costs (cloud).**
- SwitchX 720p: 3 credits per 30 frames.
- SwitchX 1080p: 10 credits per 30 frames.
- Background Remover: 1 credit per image or per video-second.
- VFX Pass Generator: 3 credits per image or per video-second.

**Practical reading for tutorials.** At Pro tier, 2,400 credits is roughly 800 thirty-frame chunks at 720p, or 240 at 1080p. A 60-second SwitchX project at 1080p / 24fps consumes about 480 credits, so the Creator tier covers ~67 seconds of 1080p SwitchX a month at 24fps and the Pro tier covers ~5 minutes. Worth grounding any "use this monthly" recommendation against these numbers so we don't accidentally recommend a tier the creator will blow past.

---

## SwitchX API (Public Beta)

**Endpoint.** `POST https://api.beeble.ai/v1/switchx/generations`.

**Auth.** `x-api-key` header.

**Request body fields (partial schema from quickstart).**
- `generation_type` (string): `"video"` or `"image"`.
- `source_uri` (string): URL to source asset.
- `reference_image_uri` (string): URL to reference image.
- `alpha_uri` (string): URL to alpha channel file.
- `alpha_mode` (string): e.g. `"custom"`.
- `max_resolution` (integer): `720` or `1080`.
- `prompt` (string): text description.

**Workflow.** Three steps: (1) upload assets, (2) create generation, (3) poll job status and download.

**Pricing.** developer.beeble.ai states "starting at $0.10 per generation." This reconciles arithmetically with cloud credit math (Pro tier values credits at ~$0.031 each; 3 credits per 30-frame 720p chunk = ~$0.094, i.e. $0.10 rounded). PROJECT_CONTEXT.md's explicit "$0.10 per 30 frames at 720p, $0.30 per 30 frames at 1080p" is consistent but not stated in those terms on the dev portal.

**Per-job frame ceiling.** PROJECT_CONTEXT.md states 240 frames max per SwitchX job. **Not directly verified at docs.** The OpenAPI spec at `docs.beeble.ai/api-reference/openapi.json` currently returns the OpenAPI Plant Store sample, not Beeble's real spec, so the documented contract is incomplete as of 2026-05-15. Treat 240 frames as the working assumption.

At common frame rates: 240 frames = 10 seconds at 24fps, 8 seconds at 30fps, 4 seconds at 60fps. A typical narrative dialogue line is 3-7 seconds, so 240 frames fits most single takes but caps long unbroken shots.

**Webhooks and idempotency.** PROJECT_CONTEXT.md states both are supported. Not yet verified at docs.

**Supported resolutions.** 720p and 1080p (matches cloud product).

---

## Integrations

Documented integration pages exist at docs.beeble.ai/integration/ for:

- **Nuke** — compositing. The Compositing Academy (Alex Hanneman) is a publicly named user.
- **Blender** — 3D pipeline.
- **Unreal Engine** — game-engine and virtual production.
- General DCC import: "Import your passes into any DCC in one step."

**Why this matters for content framing.** When a breakdown's recommendation involves taking PBR passes downstream into Nuke or Blender, naming those specifically is grounded in Beeble's own public integration docs and reads as informed rather than fabricated.

---

## Named users and recognition (for credibility-laundering when relevant)

- Boxel Studio used Beeble for relighting VFX on Superman & Lois S4.
- Compositing Academy (Alex Hanneman) uses the Nuke plugin in their curriculum.
- Named VFX artists publicly on beeble.ai: Jonathan Hislop, Suryam Singh, Joshua M. Kerr.
- 2026 Webby Awards winner.

These are useful for grounding "real studios use this" claims without name-dropping specific film titles Beeble didn't ship in.

---

## Known unknowns

These are explicit gaps in verifiable knowledge. The agent must hedge any claim that touches them.

- **Subtle preservation of practical-lit faces in two-shot dialogue blocking.** Can SwitchX hold a soft warm key on two actors' faces during a close-quarters conversation while pushing the surrounding environment into a different look? Especially relevant for Past Lives bar-scene class of shots. Plausibly yes via Fill mode with a strong reference, but the failure modes (face-light drift, identity wobble on the off-camera actor) are unknown until we run a test or see real examples.
- **Identity stability across long takes.** What happens to subject identity in a one-take dialogue scene approaching the 240-frame ceiling? Documented preservation claims are blanket and do not address duration-dependent drift.
- **Subtlety vs. boldness bias.** Generative video models tend to push toward visually richer, busier choices. Can SwitchX execute a restrained aesthetic (Kirchner-style low-contrast soft warm naturalism) or does it tend to amp things up? Unknown until tested.
- **Mask precision around edges.** Docs say "artifact-free" mattes but do not quantify SAM3 performance around hair, glasses, fabric edges, or motion blur.
- **Exact 240-frame ceiling.** Need to confirm at docs or via the real OpenAPI spec once Beeble publishes it.
- **Webhook URL format and event schema.** Claimed by PROJECT_CONTEXT.md, not in fetched docs.
- **Idempotency key header name and semantics.** Same.
- **Input file format whitelist.** What containers and codecs does `source_uri` accept? Not documented.
- **Beeble Studio public pricing.** $500/yr indie and $3,000/yr facility from PROJECT_CONTEXT.md are not on the public pricing page.
- **Image generation_type behavior.** API quickstart references `generation_type: "video"` and presumably `"image"`. What does image mode change beyond the obvious frame-count irrelevance? Resolution caps, pricing?
- **Audio handling.** Nothing in docs about sound. Presumably SwitchX is video-only and strips audio; needs confirming if a tutorial would advise dropping audio first.
- **Multi-subject identity stability.** Select mode supports multi-subject, but how well does it hold two faces simultaneously across a take?
- **Performance under heavy reference-source mismatch.** Beeble says "the reference doesn't need to perfectly match"; what's the actual tolerance before output quality collapses?

When generating content, treat each of these as a "design intent + technique + caveat + tactical note" candidate rather than an outcome to claim.

---

## Update protocol

When the agent learns something new from a fetched docs page, a verified test, or Jason's correction:

1. Find the relevant section above.
2. Add the new fact with the source (URL or "verified by Jason 2026-MM-DD").
3. Remove the matching entry from "Known unknowns" if resolved.
4. Bump the "Last refreshed" date at the top.

Do not add unverified claims. This file is the part of the agent's brain it can trust.
