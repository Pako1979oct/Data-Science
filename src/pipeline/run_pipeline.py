from __future__ import annotations

import argparse
from pathlib import Path

from src.pipeline.demo_data import write_demo_csv
from src.pipeline.run import run_pipeline
from src.pipeline.schemas import PipelineConfig


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Pipeline de ciencia de datos (CSV → modelo → métricas).")
    p.add_argument("--input", type=str, default="", help="Ruta a CSV de entrada. Si se omite, se genera demo.")
    p.add_argument("--target", type=str, default="target", help="Nombre de la columna objetivo.")
    p.add_argument("--artifacts", type=str, default="artifacts", help="Carpeta de salida para artefactos.")
    p.add_argument("--test-size", type=float, default=0.2, help="Proporción de test (0-1).")
    p.add_argument("--random-state", type=int, default=42, help="Semilla aleatoria.")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    input_csv = args.input.strip()
    if not input_csv:
        demo_path = Path("data") / "raw" / "demo.csv"
        write_demo_csv(demo_path, n=1200, random_state=args.random_state)
        input_csv = str(demo_path)

    cfg = PipelineConfig(
        input_csv=Path(input_csv),
        target_col=args.target,
        artifacts_dir=Path(args.artifacts),
        test_size=args.test_size,
        random_state=args.random_state,
    )

    result = run_pipeline(cfg)
    print("OK")
    print(f"Accuracy: {result['accuracy']:.4f}")
    print(f"Modelo:   {result['model_path']}")
    print(f"Métricas: {result['metrics_path']}")


if __name__ == "__main__":
    main()

