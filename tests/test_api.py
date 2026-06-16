from fastapi.testclient import TestClient
from api.main import app
from unittest.mock import patch

client = TestClient(app)


def test_rates_valid():
    response = client.get("/rates/livret_a")
    assert response.status_code == 200
    data = response.json()

    assert data["metric"] == "livret_a"
    assert len(data["data"]) > 0


def test_rates_invalid():
    response = client.get("/rates/invalid_metric")
    assert response.status_code == 404


def test_rates_latest():
    response = client.get("/rates/livret_a/latest")
    assert response.status_code == 200
    data = response.json()

    assert "latest" in data
    assert data["metric"] == "livret_a"


def test_real_return():
    response = client.get("/analyze/real-return?asset=livret_a&amount=10000")
    assert response.status_code == 200

    data = response.json()

    assert data["asset"] == "livret_a"
    assert data["amount"] == 10000
    assert "real_rate" in data["result"]


def test_real_return_invalid():
    response = client.get("/analyze/real-return?asset=invalid&amount=10000")
    assert response.status_code == 404


def test_compare():
    response = client.get("/analyze/compare?assets=livret_a,lep&amount=10000")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data["results"], list)
    assert len(data["results"]) >= 1


@patch("api.routers.analyze.provider.generate_analysis")
def test_get_analysis(mock_generate):
    mock_generate.return_value = "Fake analysis"

    response = client.get("/analyze/analyze?asset=livret_a&amount=10000")
    assert response.status_code == 200
    data = response.json()

    assert data["stats"]["asset"] == "livret_a"
    assert data["analysis"] == "Fake analysis"
