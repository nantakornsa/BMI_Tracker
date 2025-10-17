import pytest
from bmi_tracker import User, DatabaseJSON, get_nutrition_advice
import os
import json


# Testing bmi calculation
def test_bmi_calculation():
    user = User("Testing", 75, 175)

    expected_bmi = 24.49

    assert user.bmi == expected_bmi


def test_database_add_and_get(tmp_path):
    # สร้างไฟล์ JSON ชั่วคราว
    test_file = tmp_path / "test_data.json"
    db = DatabaseJSON(file_name=str(test_file))

    # สร้าง user จำลอง
    user = User("Alice", 60, 165)
    db.add_user(user)

    # อ่านข้อมูลย้อนหลัง
    history = db.get_user_history("Alice")

    # ควรมี 1 record
    assert len(history) == 1

    # ตรวจสอบค่า BMI
    bmi_value, record_date = history[0]
    expected_bmi = round(60 / (1.65**2), 2)
    assert bmi_value == expected_bmi


def test_get_nutrition_advice(monkeypatch):
    # mock API responseจะได้ไม่ต้อง จะได้รันโดยไม่ต้องใช้flaskจริงๆ
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"foods": ["eggs", "nuts"]}

    # แทนที่ requests.post ด้วย mock
    import requests

    monkeypatch.setattr(requests, "post", lambda *a, **k: MockResponse())

    result = get_nutrition_advice(17)  # BMI ต่ำ = underweight
    assert "eggs" in result
