from pathlib import Path

from app.config import get_config
from app.pipeline import ShortsPipeline



def test_pipeline_smoke(tmp_path: Path):
    pipeline = ShortsPipeline(config=get_config(), dry_run=True)
    out_dir = tmp_path / "package"
    pipeline.run(
        topic="Why poor people stay poor",
        tone="discipline",
        duration=60,
        n_titles=3,
        n_scenes=8,
        output_dir=str(out_dir),
    )
    expected = [
        "metadata.json",
        "titles.json",
        "script.json",
        "script.txt",
        "tts_narration.txt",
        "scenes.json",
        "subtitles.srt",
        "edit_plan.json",
        "thumbnail_copy.json",
        "qa_report.json",
    ]
    for name in expected:
        assert (out_dir / name).exists(), name

    titles_payload = (out_dir / "titles.json").read_text(encoding="utf-8")
    assert '"titles"' in titles_payload
