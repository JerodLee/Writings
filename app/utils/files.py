from __future__ import annotations

import json
from pathlib import Path
from typing import Any



def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)



def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")



def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")



def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))
