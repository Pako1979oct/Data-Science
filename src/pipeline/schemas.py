from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    input_csv: Path
    target_col: str = "target"
    artifacts_dir: Path = Path("artifacts")
    test_size: float = 0.2
    random_state: int = 42

