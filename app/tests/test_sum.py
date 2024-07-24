from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the sum API"}

def test_calculate_sum():
    response = client.post("/sum", json={"value1": 10.5, "value2": 5.5})
    assert response.status_code == 200
    assert response.json() == {"sum": 16.0}


def test_invalid_input():
    response = client.post("/sum", json={"value1": "rewrer5.5", "value2": 5.5})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "value1"],
                "msg": "Input should be a valid number, unable to parse string as a number",
                "type": "float_parsing",
                "input": "rewrer5.5"
            }
        ]
    }