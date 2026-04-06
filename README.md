# AI Faceless Finance Motivation Shorts Generator (MVP)

Generate a complete **YouTube Shorts content package** from one topic (finance + motivation + psychology, non-news).

## Features

- CLI-first pipeline (`python -m app.main ...`)
- Supports OpenAI API generation with robust fallback logic
- Full dry-run mode (no API key required)
- Outputs complete package files:
  - `metadata.json`
  - `titles.json`
  - `script.json`
  - `script.txt`
  - `tts_narration.txt`
  - `scenes.json`
  - `subtitles.srt`
  - `edit_plan.json`
  - `thumbnail_copy.json`
  - `qa_report.json`
- Built-in QA checks (structure, banned phrases, title count, duration)
- Pytest coverage for slug, subtitle format, and pipeline smoke run

## Project Structure

```text
app/
  main.py
  pipeline.py
  config.py
  cli.py
  generators/
  services/
  utils/
  templates/
data/
outputs/
tests/
README.md
requirements.txt
.env.example
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Setup

1. Copy env template:

```bash
cp .env.example .env
```

2. Add your key (optional if using dry-run):

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
APP_LOG_LEVEL=INFO
```

## Run

Required invocation:

```bash
python -m app.main --topic "Why poor people stay poor"
```

All options:

```bash
python -m app.main \
  --topic "Why poor people stay poor" \
  --tone discipline \
  --duration 60 \
  --n-titles 7 \
  --n-scenes 8 \
  --dry-run \
  --output-dir outputs/custom-package
```

### CLI Options

- `--topic` (required)
- `--tone` (`fear`, `urgency`, `discipline`, `regret`, `ambition`)
- `--duration` (default `60`)
- `--n-titles`
- `--n-scenes`
- `--dry-run`
- `--output-dir`

## Dry-Run Usage

Dry-run avoids API calls and uses deterministic local generators:

```bash
python -m app.main --topic "Why poor people stay poor" --dry-run
```

## Output Explanation

- **metadata**: run configuration and context.
- **titles**: clickable title options with score + reason.
- **script**: structured short script (hook/problem/emotion/insight/ending).
- **script.txt**: plain text narration script.
- **tts_narration.txt**: TTS-friendly lines + pause tags.
- **scenes**: scene-by-scene visual/narration guidance.
- **subtitles.srt**: subtitle timing and lines.
- **edit_plan**: 9:16 timeline for FFmpeg/CapCut workflows.
- **thumbnail_copy**: short emotional thumbnail phrases.
- **qa_report**: safety and structural validation report.

## Testing

```bash
pytest -q
```

## Expansion Ideas

- **EC2 deployment**: containerize and run scheduled batch jobs.
- **FFmpeg integration**: auto-stitch stock clips + voiceover + SRT burn-in.
- **TTS providers**: ElevenLabs/Azure/AWS Polly adapters.
- **YouTube API**: auto-upload title/description/tags/thumbnail.
- **Analytics loop**: feed retention metrics back into title/script scoring.

