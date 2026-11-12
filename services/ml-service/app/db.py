"""Registro de pronósticos en MongoDB. Si Mongo no está disponible, el servicio sigue funcionando."""
import os
from datetime import datetime, timezone

from pymongo import MongoClient

_client: MongoClient | None = None


def _collection():
    global _client
    if _client is None:
        url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        _client = MongoClient(url, serverSelectionTimeoutMS=500)
    return _client[os.getenv("MONGO_DB", "pymeinsight")]["forecasts"]


def log_forecast(sku: str | None, horizon_days: int, predictions: list[dict]) -> bool:
    try:
        _collection().insert_one({
            "sku": sku,
            "horizon_days": horizon_days,
            "predictions": predictions,
            "created_at": datetime.now(timezone.utc),
        })
        return True
    except Exception:
        return False


def recent_forecasts(limit: int = 10) -> list[dict]:
    try:
        docs = _collection().find({}, {"_id": 0}).sort("created_at", -1).limit(limit)
        return [{**d, "created_at": d["created_at"].isoformat()} for d in docs]
    except Exception:
        return []
