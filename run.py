"""CLI entry point."""

import argparse
import json
import re
import sys
from pathlib import Path

from src.shot_analyzer import analyze
from src.beeble_fit import reason_beeble_fit
from src.content_generator import generate_content, NotAFitError

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_ROOT = PROJECT_ROOT / "outputs"


def slugify(name: str) -> str:
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def main():
    parser = argparse.ArgumentParser(
        description="Beeble shot-breakdown content engine"
    )
    parser.add_argument("--shot", help="Path to reference image")
    parser.add_argument(
        "--slug",
        help="Override output slug (default: derived from filename)",
    )
    parser.add_argument(
        "--test-analyzer",
        action="store_true",
        help="Test mode: save under outputs/_test_analyzer/<slug>/",
    )
    parser.add_argument(
        "--reuse-analysis",
        action="store_true",
        help="Skip analyzer if analysis.json already exists",
    )
    parser.add_argument(
        "--reuse-fit",
        action="store_true",
        help="Skip fit reasoner if fit.json already exists",
    )
    parser.add_argument(
        "--from-analysis",
        help="Path to an existing analysis.json; skips analyzer step",
    )
    parser.add_argument(
        "--formats",
        help="Comma-separated subset of formats to generate (tiktok,reddit,xthread,youtube). Default: all four.",
    )
    parser.add_argument(
        "--skip-content",
        action="store_true",
        help="Stop after fit reasoner; do not run content generator",
    )
    args = parser.parse_args()

    if args.from_analysis:
        analysis_path = Path(args.from_analysis)
        if not analysis_path.exists():
            sys.exit(f"Analysis file not found: {analysis_path}")
        analysis = json.loads(analysis_path.read_text())
        out_dir = analysis_path.parent
        print(f"Using existing analysis: {analysis_path}", flush=True)
    else:
        if not args.shot:
            sys.exit("Must provide --shot or --from-analysis")
        shot_path = Path(args.shot)
        if not shot_path.exists():
            sys.exit(f"Shot file not found: {shot_path}")
        slug = args.slug or slugify(shot_path.stem)
        if args.test_analyzer:
            out_dir = OUTPUT_ROOT / "_test_analyzer" / slug
        else:
            out_dir = OUTPUT_ROOT / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        analysis_path = out_dir / "analysis.json"

        if args.reuse_analysis and analysis_path.exists():
            print(f"Reusing analysis: {analysis_path}", flush=True)
            analysis = json.loads(analysis_path.read_text())
        else:
            print(f"Analyzing {shot_path.name}", flush=True)
            analysis = analyze(str(shot_path))
            analysis_path.write_text(json.dumps(analysis, indent=2))
            print(f"Saved: {analysis_path}")

        if "error" in analysis:
            print(f"\nAnalyzer error: {analysis['error']}", file=sys.stderr)
            sys.exit(1)

    fit_path = out_dir / "fit.json"
    if args.reuse_fit and fit_path.exists():
        print(f"Reusing fit: {fit_path}", flush=True)
        fit = json.loads(fit_path.read_text())
    else:
        print("Reasoning Beeble fit", flush=True)
        fit = reason_beeble_fit(analysis)
        fit_path.write_text(json.dumps(fit, indent=2))
        print(f"Saved: {fit_path}")

    if "error" in fit:
        print(f"\nFit reasoner error: {fit['error']}", file=sys.stderr)
        sys.exit(1)

    if not fit.get("is_fit"):
        reasoning = fit.get("fit_reasoning", "(no reasoning returned)")
        print(f"\nis_fit=false. Pipeline stops. Content generator will not run.")
        print(f"Reason: {reasoning}")
        return

    if args.skip_content:
        print("\nis_fit=true. Stopping per --skip-content.")
        return

    formats = None
    if args.formats:
        formats = [f.strip() for f in args.formats.split(",") if f.strip()]

    print(f"\nGenerating content ({', '.join(formats) if formats else 'all formats'})", flush=True)
    try:
        contents = generate_content(analysis, fit, formats=formats)
    except NotAFitError as e:
        print(f"\n{e}", file=sys.stderr)
        sys.exit(1)

    for fmt, body in contents.items():
        out_path = out_dir / f"{fmt}.md"
        out_path.write_text(body + "\n")
        print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
