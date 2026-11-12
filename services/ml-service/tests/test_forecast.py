from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from app.forecast import demo_history, forecast
from app.main import app

client = TestClient(app)


def test_forecast_devuelve_horizonte_pedido_y_no_negativo():
    hist = demo_history("CAF-001", days=60, today=date(2026, 11, 1))
    out = forecast(hist, 7)
    assert len(out) == 7
    assert out[0][0] == hist[-1][0] + timedelta(days=1)
    assert all(u >= 0 for _, u in out)


def test_forecast_captura_efecto_fin_de_semana():
    # Ventas: 10 entre semana, 20 en fin de semana, sin ruido.
    start = date(2026, 9, 1)
    hist = [(start + timedelta(days=i), 20.0 if (start + timedelta(days=i)).weekday() >= 5 else 10.0)
            for i in range(56)]
    out = forecast(hist, 7)
    weekend = [u for d, u in out if d.weekday() >= 5]
    weekday = [u for d, u in out if d.weekday() < 5]
    assert min(weekend) > max(weekday)


def test_historial_corto_falla():
    with pytest.raises(ValueError):
        forecast([(date(2026, 1, 1), 5.0)], 7)


def test_endpoint_demo_responde():
    r = client.get("/forecast/demo/TE-014?horizon_days=5")
    assert r.status_code == 200
    assert len(r.json()["predictions"]) == 5


def test_endpoint_rechaza_historial_corto():
    r = client.post("/forecast", json={"history": [{"date": "2026-01-01", "units": 3}], "horizon_days": 7})
    assert r.status_code == 422
