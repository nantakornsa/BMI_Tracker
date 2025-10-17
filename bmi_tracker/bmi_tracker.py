import json
from datetime import date
import matplotlib.pyplot as plt
import requests
import os

JSON_FILE = "bmi_data.json"


# ==========================
# 1️⃣ User Class
# ==========================
class User:
    def __init__(self, name, weight, height):
        self.name = name
        self.weight = weight
        self.height = height
        self.bmi = self.calculate_bmi()

    def calculate_bmi(self):
        return round(self.weight / ((self.height / 100) ** 2), 2)


# ==========================
# 2️⃣ Database Class (JSON)
# ==========================
class DatabaseJSON:
    def __init__(self, file_name=JSON_FILE):
        self.file_name = file_name
        if not os.path.exists(file_name):
            with open(file_name, "w") as f:
                json.dump({}, f)  # สร้างไฟล์ว่าง

    def add_user(self, user: User):
        data = self._load_data()
        user_data = {
            "weight": user.weight,
            "height": user.height,
            "bmi": user.bmi,
            "record_date": str(date.today()),
        }
        if user.name not in data:
            data[user.name] = []
        data[user.name].append(user_data)
        self._save_data(data)

    def get_user_history(self, name):
        data = self._load_data()
        if name in data:
            return [(entry["bmi"], entry["record_date"]) for entry in data[name]]
        return []

    def _load_data(self):
        with open(self.file_name, "r") as f:
            return json.load(f)

    def _save_data(self, data):
        with open(self.file_name, "w") as f:
            json.dump(data, f, indent=4)


# ==========================
# 3️⃣ API Integration
# ==========================
def get_nutrition_advice(bmi):
    url = "http://127.0.0.1:5000/nutrition"  # mock API URLที่สร้างเองงงงงง
    try:
        response = requests.post(
            url, json={"bmi": bmi}
        )  # ส่งข้อมูล BMI ไปในรูปแบบ JSON เช่น:
        response.raise_for_status()  # ถ้ามี error จะโยน exception
        foods = response.json()["foods"]
        return f"Suggested food: {', '.join(foods)}"
    except requests.exceptions.RequestException:
        return "Unable to fetch nutrition advice right now."


# ==========================
# 4️⃣ Visualization
# ==========================
def plot_bmi_trend(history, username):
    if not history:
        print("No history to plot.")
        return
    bmis, dates = zip(*history)
    plt.plot(dates, bmis, marker="o")
    plt.title(f"BMI Trend for {username}")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.grid(True)
    plt.show()


# ==========================
# 5️⃣ Main Program
# ==========================
def main():
    print("=== BMI Tracker with Nutrition Advice (JSON) ===")
    name = input("Enter your name: ")
    weight = float(input("Enter your weight (kg): "))
    height = float(input("Enter your height (cm): "))

    user = User(name, weight, height)
    print(f"\nHello, {user.name}! Your BMI is {user.bmi}")

    if user.bmi < 18.5:
        print("You're underweight.")
    elif user.bmi < 25:
        print("You're normal weight.")
    elif user.bmi < 30:
        print("You're overweight.")
    else:
        print("You're obese.")

    db = DatabaseJSON()
    db.add_user(user)

    history = db.get_user_history(name)
    plot_bmi_trend(history, name)

    print("\nFetching nutrition advice...")
    print(get_nutrition_advice(user.bmi))


if __name__ == "__main__":
    main()
