"""Pronóstico de demanda diaria con scikit-learn (Ridge sobre tendencia + día de la semana)."""
import zlib
from datetime import date, timedelta

import numpy as np
from sklearn.linear_model import Ridge

MIN_HISTORY_DAYS = 14


def _features(day_index: np.ndarray, weekdays: np.ndarray) -> np.ndarray:
    return np.column_stack([day_index, np.eye(7)[weekdays]])


def forecast(history: list[tuple[date, float]], horizon_days: int) -> list[tuple[date, float]]:
    """Predice las unidades vendidas por día para los próximos `horizon_days`."""
    if len(history) < MIN_HISTORY_DAYS:
        raise ValueError(f"Se necesitan al menos {MIN_HISTORY_DAYS} días de historial.")

    history = sorted(history, key=lambda p: p[0])
    start = history[0][0]
    idx = np.array([(d - start).days for d, _ in history])
    wd = np.array([d.weekday() for d, _ in history])
    y = np.array([u for _, u in history], dtype=float)

    model = Ridge(alpha=1.0).fit(_features(idx, wd), y)

    last = history[-1][0]
    future = [last + timedelta(days=i) for i in range(1, horizon_days + 1)]
    f_idx = np.array([(d - start).days for d in future])
    f_wd = np.array([d.weekday() for d in future])
    preds = np.clip(model.predict(_features(f_idx, f_wd)), 0, None)

    return [(d, round(float(p), 1)) for d, p in zip(future, preds)]


def demo_history(sku: str, days: int = 60, today: date | None = None) -> list[tuple[date, float]]:
    """Historial sintético y determinista por SKU (hasta que core-api registre ventas reales)."""
    rng = np.random.default_rng(zlib.crc32(sku.encode()))
    base = float(rng.integers(3, 12))
    trend = float(rng.uniform(0.0, 0.08))
    weekend_boost = float(rng.uniform(1.2, 1.8))
    end = today or date.today()
    out: list[tuple[date, float]] = []
    for i in range(days):
        d = end - timedelta(days=days - i)
        mult = weekend_boost if d.weekday() >= 5 else 1.0
        units = max(0.0, (base + trend * i) * mult + float(rng.normal(0, 1.0)))
        out.append((d, round(units, 1)))
    return out
