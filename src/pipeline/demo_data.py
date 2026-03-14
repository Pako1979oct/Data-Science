from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .io_utils import ensure_dir


def make_demo_dataset(n: int = 1200, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    age = rng.integers(18, 70, size=n)
    income = rng.normal(35000, 12000, size=n).clip(5000, 150000)
    city = rng.choice(["CDMX", "GDL", "MTY", "PUE", "QRO"], size=n, p=[0.35, 0.2, 0.2, 0.15, 0.1])
    channel = rng.choice(["web", "tienda", "telefono"], size=n, p=[0.55, 0.35, 0.1])
    tenure_months = rng.integers(0, 120, size=n)

    # Probabilidad sintética (clasificación binaria)
    score = (
        0.03 * (age - 40)
        + 0.00004 * (income - 35000)
        + 0.012 * (tenure_months - 24)
        + (city == "CDMX") * 0.25
        + (channel == "web") * 0.2
        - (channel == "telefono") * 0.15
        + rng.normal(0, 0.5, size=n)
    )
    prob = 1 / (1 + np.exp(-score))
    target = (prob >= 0.5).astype(int)

    df = pd.DataFrame(
        {
            "age": age,
            "income": income.round(2),
            "city": city,
            "channel": channel,
            "tenure_months": tenure_months,
            "target": target,
        }
    )

    # Mete algunos faltantes para probar imputación
    miss_idx = rng.choice(n, size=int(0.03 * n), replace=False)
    df.loc[miss_idx, "income"] = np.nan
    miss_idx2 = rng.choice(n, size=int(0.02 * n), replace=False)
    df.loc[miss_idx2, "city"] = None
    return df


def write_demo_csv(path: str | Path, n: int = 1200, random_state: int = 42) -> Path:
    p = Path(path)
    ensure_dir(p.parent)
    df = make_demo_dataset(n=n, random_state=random_state)
    df.to_csv(p, index=False)
    return p

