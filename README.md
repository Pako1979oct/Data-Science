# Pipeline de ciencia de datos (Python)

Este proyecto incluye un pipeline reproducible de ciencia de datos:

- Ingesta (CSV)
- Validación de columnas
- Limpieza
- Ingeniería de características (numéricas + categóricas)
- Entrenamiento (baseline con `LogisticRegression`)
- Evaluación (accuracy + classification report)
- Persistencia (modelo + métricas)

## Requisitos

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar demo end-to-end

Esto genera un dataset sintético, lo guarda en `data/raw/demo.csv`, entrena, evalúa y guarda el modelo en `artifacts/`.

```bash
python run_pipeline.py
```

## Usar tu propio CSV

Coloca un CSV con una columna objetivo (por defecto: `target`) y ejecuta:

```bash
python run_pipeline.py --input data/raw/tu_archivo.csv --target target
```

Los artefactos se guardan en:

- `artifacts/model.joblib`
- `artifacts/metrics.json`

