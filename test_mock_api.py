import json
from mock_api import app


def test_get_nutrition():
    client = app.test_client()
    response = client.get("/nutrition/normal")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "foods" in data
    assert "balanced meal" in data["foods"][0]


def test_post_nutrition_underweight():
    client = app.test_client()
    response = client.post("/nutrition", json={"bmi": 17})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "chicken breast" in data["foods"][0]


def test_post_nutrition_overweight():
    client = app.test_client()
    response = client.post("/nutrition", json={"bmi": 30})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "salad" in data["foods"][1]
