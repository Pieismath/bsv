# PROJECT_CONTEXT.md

> **Read this file in full before doing anything.** It is the single source of truth for what we are building and why. Do not deviate from the framing here without asking.

---

## What this project is

This is a **prototype GTM agent for Beeble AI**, built as a written project submission for the **Basis Set Ventures AI Fellow** interview. Basis Set Ventures (BSV) is the venture firm running the interview process and is also Beeble's lead seed investor — so this work is being read by people who know Beeble well.

The submission has three deliverables: a prioritization framework across ~15 startups, a deep-dive on one company with a working agent prototype, and a raw LLM conversation transcript showing how I worked through ambiguity. You (Claude Code) are helping with the second deliverable: the agent and its outputs.

**The single most important evaluation criterion BSV stated:** "We are evaluating you on the taste/intuition behind the output, as well as the mechanisms behind your agent to deliver the output at scale." Taste matters as much as code quality. Generic AI marketing slop is worse than no output at all.

---

## About Beeble (target company)

Beeble (beeble.ai) is a Seoul-based VFX startup founded in 2022 by five ex-Krafton AI researchers. They raised a $4.75M seed led by Basis Set Ventures + Fika Ventures in 2024. Their thesis: AI-driven relighting and compositing democratize Hollywood-grade VFX for indie filmmakers, content creators, and small studios.

**Products (as of mid-2026):**
- **SwitchLight 3.0** — video-to-PBR model that turns any 2D footage into physically based rendering passes (normals, base color, roughness, depth, etc.). Lets you relight any video in post as if it were CG.
- **SwitchX** — video-to-video generative model that swaps backgrounds, lighting, props, and environments while keeping the original subject (face, motion, identity) intact. The hero product for creators.
- **Beeble Cloud** — browser-based web app; credit system (Free 90/mo, Creator $19/mo for 540 credits, Pro $75/mo for 2,400 credits).
- **Beeble Studio** — desktop app running SwitchLight 3.0 locally on GPU; for facilities that need privacy/4K/unlimited rendering. $500/yr indie, $3,000/yr facility.
- **SwitchX API (public beta, ~April 2026)** — REST endpoint for SwitchX. $0.10/30 frames at 720p, $0.30/30 frames at 1080p. Supports webhooks, idempotency, base64 or URL uploads, 240-frame max per job. This matters: it makes Beeble pipeline-integratable, not just a browser tool.

**Customers today:** Used by Oscar-winning studios (top-down) and indie creators (bottom-up). The squeeze: the middle of the market (small commercial shops, music video directors, YouTube cinematography channels, indie filmmakers) is the biggest untapped lane.

**Competitive landscape:** Runway, Sora, Pika (generative video, less precise control); Wonder Dynamics (3D character replacement); Nuke / DaVinci / After Effects (traditional VFX pipelines they integrate with). Beeble's edge is *control* — every other AI video tool throws creativity to the model; Beeble preserves the original footage and only changes what you tell it to.

---

## The growth problem this agent solves

**Lane: indie filmmaker + creator acquisition via filmmaker-native content.**

Beeble's product is strong and their enterprise sales motion is healthy. Their actual GTM gap is the **middle of the funnel** — the indie filmmaker, the one-person commercial shop, the music video director, the YouTube cinematography channel, the r/filmmakers regular. These people:

- Don't read TechCrunch and aren't reached by ads
- Learn from other filmmakers, mostly through *shot breakdowns* and BTS content on YouTube, TikTok, Instagram, and Reddit
- Have real budget ($19–$75/mo is nothing for a working creative) but only convert when the product is shown to them by someone they trust
- Care intensely about craft — generic "AI is amazing!" content actively repels them

The content genre that already wins this audience is the **shot breakdown** — videos and posts that analyze a famous shot, explain how it was lit, blocked, and composed, then show how to recreate it. Channels like Wolfcrawler, In Depth Cine, and the StudioBinder blog rack up millions of views on this format.

**Insight:** Beeble's product *is* shot manipulation. A shot breakdown that ends with "and here's how to do this in your bedroom with Beeble" is not a marketing ad — it is genuinely useful filmmaker education that happens to demo the product perfectly. The agent's job is to produce these at scale, across formats, with taste.

---

## What we are building

A **multi-format shot breakdown content engine** for Beeble. The agent:

**Inputs:**
- A reference (URL, uploaded image/video, or text description) of a notable shot — a famous film still, a viral commercial moment, a music video frame, an iconic music video, etc.
- Optional: target channel(s) — e.g. "make me a TikTok script + Reddit post + X thread for this"

**Pipeline (planned):**
1. **Shot analyst** — uses vision-capable LLM to analyze the reference shot: lighting (key/fill/back, color temp, hard vs soft, motivation), composition, mood, time of day, environment. Identifies what would be expensive/impossible for an indie creator to replicate the traditional way.
2. **Beeble-fit reasoner** — determines what is genuinely Beeble-relevant about this shot (does it require relighting? background swap? environment change? if nothing fits Beeble's product, the agent flags it and stops — we are not generating fake claims).
3. **Tutorial planner** — outlines a realistic recreation: what you'd shoot at home, what you'd change in Beeble (specific SwitchX prompt, what reference image to feed it, what to mask), expected result.
4. **Multi-format writer** — produces channel-specific outputs from the same plan:
   - 45-60s TikTok / Reels / YouTube Short script (hook, demo, payoff, CTA)
   - r/filmmakers Reddit post (tutorial-first, not promotional; Reddit-native voice)
   - X / Twitter thread (5-8 posts, hook + breakdown + before/after)
   - Longer YouTube video script outline (3-5 min)
5. **(Stretch) SwitchX API integration** — actually call Beeble's SwitchX API on a sample input to produce a real before/after visual, attached to the content.

**Outputs:** a folder per shot containing all formats, ready to copy/paste, plus any generated visuals.

**Polished example outputs to ship in the writeup:** 2-4 fully realized shot breakdowns across formats, picking shots that play to Beeble's specific strengths (one strong relighting example, one strong background-swap example, ideally one that's seasonally relevant or culturally hot at submission time).

---

## Voice and taste guidelines

This is the part that matters most. Read it twice.

**The voice is filmmaker-to-filmmaker, never marketer-to-customer.**

- Write like someone who has actually held a camera. Mention specific equipment when relevant (Aputure 600d, Litepanels Gemini, RGB tubes). Use real cinematography terminology: motivated lighting, practicals, hard vs soft sources, color contrast, negative fill, eye light, top light.
- Reference real cinematographers when natural: Deakins, Lubezki, Khondji, Chivo, Sayombhu Mukdeeprom, Greig Fraser, Hoyte van Hoytema, Linus Sandgren. Don't name-drop for cred — only when the comparison is earned.
- No filler phrases. No "in today's fast-paced world." No "unlock the power of." No "harness the magic of AI." No "revolutionize." No "game-changer."
- No em dashes. Use commas, parentheses, or periods. (This is a personal style preference but it also makes the writing sound less LLM-generated, which is the whole point.)
- Reddit posts must sound like Reddit posts. Lowercase titles often. Self-deprecating. Show the work, including what didn't work. Mention specific gear/software. The CTA at the end should be soft — "here's the tool I used, decide for yourself" not "click here to learn more."
- TikTok / Reels scripts: hook in the first 1.5 seconds, must work without sound, end with a visual payoff not a CTA card.
- X threads: short posts, no thread-bro tics ("Here's how 🧵👇" or "A thread:" or "Let me break it down"). Just start with the most interesting frame and earn the next click.

**The taste filter:** before any output ships, ask: "would a working DP/filmmaker post this themselves, or would they cringe?" If it's the second one, redo it.

**What we are NOT doing:**
- Generic "5 ways AI is changing filmmaking" listicles
- Hype copy ("the future of VFX is here")
- Anything that sounds like it came from a SaaS marketing intern
- Lying about what Beeble can do. If a shot needs something Beeble can't deliver, we either pick a different shot or honestly note the limitation

---

## Technical preferences

- **Language:** Python preferred (Jason is fluent; cleanest for orchestration + API work). TypeScript acceptable if there's a strong reason.
- **LLM:** Use Claude (anthropic SDK) as the primary reasoning model since this is a BSV/Anthropic-ecosystem project. Use Claude with vision for shot analysis.
- **Structure:** single repo, modular. Each pipeline step should be its own file/function. Easy to swap out individual steps.
- **No heavyweight frameworks** unless they save real time. No LangChain unless we have a specific reason. Direct API calls with clean abstractions are better.
- **Config:** keep prompts in a `prompts/` directory as `.md` files, not hardcoded strings in Python. Easier to iterate on prompt engineering.
- **Outputs:** save to `outputs/<shot_slug>/` with one file per format. Each output is plain markdown or text, ready to copy.
- **No production polish.** This is a prototype. Don't add auth, rate limiting, error retries beyond basics, telemetry, or deployment configs. Make it runnable from the command line.
- **Demo-able.** Final state should let me run `python run.py --shot "url or description"` and watch it produce a folder of polished content.

---

## What "good" looks like for this submission

If we ship this and BSV reads it, the reaction we want is: "this person actually has taste, knows the audience, and can build the system that operationalizes it." Not "this person built a sophisticated agent." The agent is the means; the *outputs* are what they'll judge.

A useful mental test: imagine the final shot breakdown gets posted to r/filmmakers under a real Beeble employee's name. Would it land? Would it get upvotes, real comments, real signups? If yes, we did it right.

---

## Hard constraints

- Do not invent Beeble features. If you don't know whether Beeble can do something, ask before writing copy that claims it.
- Do not generate content using real public figures' names in fabricated ways. Referencing a film and its DP factually is fine. Putting words in their mouths is not.
- Do not produce content that would embarrass Beeble or BSV. When in doubt, ask.
- Keep the prototype scope tight. Better to ship one excellent pipeline than four half-built ones.

---

## How to work with me (Jason)

- I'll give you tasks one at a time. Don't run ahead and build five things when I asked for one.
- If something I ask for conflicts with this doc, point that out before doing it.
- If you have a better idea than what I asked, propose it before building it.
- I prefer plain prose explanations over bullet-list summaries when you're thinking through a decision. Save bullets for actual lists of options/files/steps.
- Show your reasoning when you make a non-obvious technical choice (library pick, abstraction boundary, etc).
