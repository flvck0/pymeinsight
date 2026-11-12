from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from . import db
from .forecast import demo_history, forecast

app = FastAPI(title="PymeInsight ML Service", version="0.1.0")


class SalesPoint(BaseModel):
    date: date
    units: float = Field(ge=0)


class ForecastRequest(BaseModel):
    history: list[SalesPoint]
    horizon_days: int = Field(default=7, ge=1, le=30)


class DayForecast(BaseModel):
    date: date
    units: float


class ForecastResponse(BaseModel):
    sku: str | None = None
    horizon_days: int
    predictions: list[DayForecast]


def _run(sku: str | None, history: list[tuple[date, float]], horizon: int) -> ForecastResponse:
    try:
        result = forecast(history, horizon)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    preds = [DayForecast(date=d, units=u) for d, u in result]
    db.log_forecast(sku, horizon, [{"date": p.date.isoformat(), "units": p.units} for p in preds])
    return ForecastResponse(sku=sku, horizon_days=horizon, predictions=preds)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/forecast", response_model=ForecastResponse)
def post_forecast(req: ForecastRequest):
    return _run(None, [(p.date, p.units) for p in req.history], req.horizon_days)


@app.get("/forecast/demo/{sku}", response_model=ForecastResponse)
def demo_forecast(sku: str, horizon_days: int = 7):
    if not 1 <= horizon_days <= 30:
        raise HTTPException(status_code=422, detail="horizon_days debe estar entre 1 y 30.")
    return _run(sku, demo_history(sku), horizon_days)


@app.get("/forecasts/recent")
def recent():
    return db.recent_forecasts()
