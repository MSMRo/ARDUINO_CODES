import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Arduino Codes Made Easy" in data["message"]


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["stats"]["total_peripherals"] >= 10
    assert data["stats"]["total_code_examples"] >= 10


def test_list_peripherals():
    response = client.get("/api/v1/peripherals")
    assert response.status_code == 200
    peripherals = response.json()
    assert len(peripherals) >= 10
    slugs = [p["slug"] for p in peripherals]
    assert "usart" in slugs
    assert "spi" in slugs
    assert "twi" in slugs
    assert "timers" in slugs
    assert "pwm" in slugs
    assert "adc" in slugs


def test_get_single_peripheral():
    response = client.get("/api/v1/peripherals/usart")
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "usart"
    assert "USART" in data["name"]
    assert data["details"] is not None
    assert len(data["code_examples"]) >= 2
    assert len(data["libraries"]) >= 1


def test_search_code():
    response = client.get("/api/v1/codes?q=Serial")
    assert response.status_code == 200
    codes = response.json()
    assert len(codes) >= 1
    assert any("Serial" in c["title"] or "Serial" in c["code"] for c in codes)


def test_categories():
    response = client.get("/api/v1/peripherals/categories")
    assert response.status_code == 200
    cats = response.json()
    assert "Serial Communication" in cats
    assert "Timing & PWM" in cats
