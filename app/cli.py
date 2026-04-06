from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shorts-generator",
        description="Generate an AI faceless finance motivation Shorts content package.",
    )
    parser.add_argument("--topic", required=True, help="Main short topic")
    parser.add_argument(
        "--tone",
        choices=["fear", "urgency", "discipline", "regret", "ambition"],
        default="discipline",
        help="Emotional tone",
    )
    parser.add_argument("--duration", type=int, default=60, help="Target duration in seconds")
    parser.add_argument("--n-titles", type=int, default=7, help="Number of titles to generate")
    parser.add_argument("--n-scenes", type=int, default=8, help="Number of scenes (6-10)")
    parser.add_argument("--dry-run", action="store_true", help="Run with no API calls")
    parser.add_argument("--output-dir", default=None, help="Override output directory")
    return parser
