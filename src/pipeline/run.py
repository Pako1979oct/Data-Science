from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import joblib

from .io_utils import ensure_dir, write_json
from .schemas import PipelineConfig
from .steps import (
    basic_cleaning,
    build_model,
    evaluate,
    load_csv,
    split_xy,
    validate_columns,
)


def run_pipeline(cfg: PipelineConfig) -> dict:
    df = load_csv(str(cfg.input_csv))
    df = basic_cleaning(df)
    validate_columns(df, required=[cfg.target_col])

    prepared = split_xy(
        df=df, target_col=cfg.target_col, test_size=cfg.test_size, random_state=cfg.random_state
    )

    model = build_model(prepared.numeric_cols, prepared.categorical_cols)
    model.fit(prepared.X_train, prepared.y_train)

    ev = evaluate(model, prepared.X_test, prepared.y_test)

    artifacts_dir = ensure_dir(cfg.artifacts_dir)
    model_path = artifacts_dir / "model.joblib"
    metrics_path = artifacts_dir / "metrics.json"
    config_path = artifacts_dir / "run_config.json"

    joblib.dump(model, model_path)
    write_json(metrics_path, {"accuracy": ev.accuracy, "classification_report": ev.report})
    write_json(
        config_path,
        {
            "input_csv": str(Path(cfg.input_csv)),
            "target_col": cfg.target_col,
            "artifacts_dir": str(Path(cfg.artifacts_dir)),
            "test_size": cfg.test_size,
            "random_state": cfg.random_state,
        },
    )

    return {
        "model_path": str(model_path),
        "metrics_path": str(metrics_path),
        "config_path": str(config_path),
        "accuracy": ev.accuracy,
        "n_rows": int(df.shape[0]),
        "n_features": int(df.shape[1] - 1),
        "prepared": {
            "numeric_cols": prepared.numeric_cols,
            "categorical_cols": prepared.categorical_cols,
        },
    }

