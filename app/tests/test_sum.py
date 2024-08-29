from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the sum API - Tiago v2.5"}

def test_calculate_sum():
    response = client.post("/sum", json={"value1": 10.5, "value2": 5.5})
    assert response.status_code == 200
    assert response.json() == {"sum": 16.0}

def test_sum_zero():
    response = client.post("/sum", json={"value1": 0, "value2": 0})
    assert response.status_code == 200
    assert response.json() == {"sum": 0}

def test_sum_negative_values():
    response = client.post("/sum", json={"value1": -10.5, "value2": -5.5})
    assert response.status_code == 200
    assert response.json() == {"sum": -16.0}

def test_sum_large_values():
    response = client.post("/sum", json={"value1": 1e10, "value2": 1e10})
    assert response.status_code == 200
    assert response.json() == {"sum": 2e10}

def test_invalid_input_non_numeric():
    response = client.post("/sum", json={"value1": "rewrer5.5", "value2": 5.5})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid number, unable to parse string as a number"

def test_invalid_input_missing_value1():
    response = client.post("/sum", json={"value2": 5.5})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "value1"]

def test_invalid_input_missing_value2():
    response = client.post("/sum", json={"value1": 5.5})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "value2"]

def test_invalid_input_extra_field():
    response = client.post("/sum", json={"value1": 5.5, "value2": 5.5, "value3": 10})
    assert response.status_code == 200  # FastAPI will ignore the extra field and process the request normally
    assert response.json() == {"sum": 11.0}

def test_invalid_input_empty_body():
    response = client.post("/sum", json={})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "value1"]
    assert response.json()["detail"][1]["loc"] == ["body", "value2"]

def test_invalid_input_no_body():
    response = client.post("/sum")
    assert response.status_code == 422
    assert "detail" in response.json()