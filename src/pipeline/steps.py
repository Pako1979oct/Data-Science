from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class DataValidationError(ValueError):
    pass


def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def validate_columns(df: pd.DataFrame, required: Iterable[str]) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise DataValidationError(f"Faltan columnas requeridas: {missing}")


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    # Normaliza nombres, elimina duplicados, recorta strings
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    df = df.drop_duplicates()
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype("string").str.strip()
    return df


@dataclass(frozen=True)
class PreparedData:
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series
    numeric_cols: list[str]
    categorical_cols: list[str]


def split_xy(df: pd.DataFrame, target_col: str, test_size: float, random_state: int) -> PreparedData:
    y = df[target_col]
    X = df.drop(columns=[target_col])

    numeric_cols = X.select_dtypes(include=["number", "bool"]).columns.tolist()
    categorical_cols = [c for c in X.columns if c not in numeric_cols]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y if y.nunique() <= 20 else None
    )
    return PreparedData(
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        numeric_cols=numeric_cols,
        categorical_cols=categorical_cols,
    )


def build_model(numeric_cols: list[str], categorical_cols: list[str]) -> Pipeline:
    numeric_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("ohe", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, numeric_cols),
            ("cat", categorical_pipe, categorical_cols),
        ],
        remainder="drop",
    )

    clf = LogisticRegression(max_iter=2000)

    model = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("clf", clf),
        ]
    )
    return model


@dataclass(frozen=True)
class EvaluationResult:
    accuracy: float
    report: dict


def evaluate(model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> EvaluationResult:
    preds = model.predict(X_test)
    acc = float(accuracy_score(y_test, preds))
    rep = classification_report(y_test, preds, output_dict=True, zero_division=0)
    return EvaluationResult(accuracy=acc, report=rep)

