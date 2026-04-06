from __future__ import annotations

import logging

from app.cli import build_parser
from app.config import get_config
from app.pipeline import ShortsPipeline


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    config = get_config()
    logging.basicConfig(level=getattr(logging, config.log_level.upper(), logging.INFO))

    pipeline = ShortsPipeline(config=config, dry_run=args.dry_run)
    out_path = pipeline.run(
        topic=args.topic,
        tone=args.tone,
        duration=args.duration,
        n_titles=args.n_titles,
        n_scenes=args.n_scenes,
        output_dir=args.output_dir,
    )
    print(f"Generated package in: {out_path}")


if __name__ == "__main__":
    main()
