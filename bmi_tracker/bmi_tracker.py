from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import os
from datetime import date
import requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


def plot_bmi_to_base64(history, username):
    if not history:
        return None

    bmis, dates = zip(*history)
    plt.figure()
    plt.plot(dates, bmis, marker="o")
    plt.title(f"BMI Trend for {username}")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.grid(True)

    # บันทึกเป็น BytesIO แล้วแปลงเป็น base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()  # ปิด figure เพื่อไม่ให้ memory leak
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return img_base64


# -----------------------------
# FastAPI
# -----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="bmi_tracker/templates")
app.mount("/static", StaticFiles(directory="bmi_tracker/static"), name="static")

# -----------------------------
# Database
# -----------------------------
JSON_FILE = "bmi_data.json"

class User:
    def __init__(self, name, weight, height):
        self.name = name
        self.weight = weight
        self.height = height
        self.bmi = round(self.weight / ((self.height / 100) ** 2), 2)

class DatabaseJSON:
    def __init__(self, file_name=JSON_FILE):
        self.file_name = file_name
        if not os.path.exists(file_name):
            with open(file_name, "w") as f:
                json.dump({}, f)

    def add_user(self, user: User):
        data = self._load_data()
        user_data = {
            "weight": user.weight,
            "height": user.height,
            "bmi": user.bmi,
            "record_date": str(date.today())
        }
        if user.name not in data:
            data[user.name] = []
        data[user.name].append(user_data)
        self._save_data(data)

    def get_user_history(self, name):
        data = self._load_data()
        return [(entry["bmi"], entry["record_date"]) for entry in data.get(name, [])]

    def _load_data(self):
        with open(self.file_name, "r") as f:
            return json.load(f)

    def _save_data(self, data):
        with open(self.file_name, "w") as f:
            json.dump(data, f, indent=4)

db = DatabaseJSON()

# -----------------------------
# Nutrition Advice
# -----------------------------
def get_nutrition_advice(bmi):
    # ใช้ URL ของ FastAPI service เอง
    url = "https://bmi-tracker-final.onrender.com"  # <-- เปลี่ยนเป็น URL จริงของคุณ!
    try:
        response = requests.post(url, json={"bmi": bmi})
        response.raise_for_status()
        foods = response.json().get("foods", [])
        return f"Suggested food: {', '.join(foods)}"
    except Exception as e:
        print("Error fetching nutrition advice:", e)
        return "Unable to fetch nutrition advice right now."
# -----------------------------
# Web Routes
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/calculate", response_class=HTMLResponse)
def calculate_bmi(request: Request, weight: float = Form(...), height: float = Form(...), name: str = Form(...)):
    user = User(name, weight, height)
    
    # เพิ่ม user ลง database
    db = DatabaseJSON()
    db.add_user(user)

    # ดึงประวัติ
    history = db.get_user_history(name)

    # สร้างกราฟเป็น base64 (ตรวจสอบ history)
    bmi_chart = plot_bmi_to_base64(history, name) if history else None
    
    # ส่งค่า nutriton ไปยัง templstes
    nutrition = get_nutrition_advice(user.bmi)

    # ส่งค่าไป template
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "name": name,
            "bmi": round(user.bmi, 2),
            "bmi_chart": bmi_chart,
            "nutrition": nutrition
        }
    )
    
class BMIRequest(BaseModel):
    bmi: float
    
@app.post("/api/nutrition")
def nutrition_api(data: BMIRequest):
    bmi = data.bmi
    if bmi < 18.5:
        category = "underweight"
    elif bmi < 25:
        category = "normal"
    else:
        category = "overweight"

    nutrition_data = {
        "underweight": ["chicken breast", "eggs", "nuts"],
        "normal": ["balanced meal with rice, veggies, protein"],
        "overweight": ["steamed vegetables", "salad", "lean protein"],
    }
    return {"foods": nutrition_data[category]}

