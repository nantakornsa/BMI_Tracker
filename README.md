# BMI-Tracker

โปรเจกต์ **BMI-Tracker-SUMMERIZER** เป็นแอป Python สำหรับติดตามค่า BMI ของผู้ใช้ พร้อมสรุปผลและกราฟสถิติ

---

## 🏷 Features

- **เพิ่มผู้ใช้ (Add User)**  
  ใส่ชื่อ น้ำหนัก ส่วนสูง คำนวณ BMI อัตโนมัติ
- **ดูประวัติผู้ใช้ (View User History)**  
  แสดงข้อมูลทั้งหมดที่บันทึกไว้ พร้อมวันเวลา
- **สรุปผล BMI (BMI Summary)**  
  แสดงค่า BMI ล่าสุดและสถานะน้ำหนัก: ต่ำ, ปกติ, เกิน, อ้วน
- **กราฟสถิติ (Visualize BMI)**  
  วาดกราฟ BMI ของผู้ใช้ตามช่วงเวลา (ใช้ `matplotlib`)
- **จัดเก็บข้อมูล .json**  
  ข้อมูลถูกเก็บในไฟล์ `users.json`


---

## 📂 Project Structure
```bash
BMI-Tracker-SUMMERIZER/
├── bmi_tracker.py          # โค้ดหลักสำหรับจัดการผู้ใช้และคำนวณ BMI
├── static/
│   └── style.css           # ตกแต่งหน้าเว็บเพจ
├── templates/
│   └── index.html          # หน้าเว็บเพจ
├── requirements.txt        # รายการ library ที่ต้องติดตั้ง
├── mock_api.py             # API ที่สร้างขึ้นมา 
├── README.md               # เอกสารอธิบายโปรเจกต์                
├── bmi_data.json           # เก็ยข้อมูลโดยใช้ .json
│   └── helpers.py
└── test_bmi_tracker.py/    # โค้ดสำหรับทดสอบโปรเจค
└── test_mock_api.py/       # โค้ดสำหรับทดสอบ API ของโปรเจค

```
---

## 💻 Installation

1. Clone โปรเจกต์จาก GitHub

```bash
git clone https://github.com/nantakornsa/BMI-Tracker-SUMMERIZER.git
cd BMI-Tracker-SUMMERIZER
```

2. รันโปรแกรมหลัก
- ทำการรันเซิร์ฟเวอร์ก่อน
- python mock_api.py
- ปิดเทอมินอลแล้วทำการรันโปรแกรม
- python BMI-Tracker.py
3. การทำงานของโปรแกรม
- จะให้ทำการกรอกข้อมูล
-   ชื่อ :
-  น้ำหนัก :
- ส่วนสูง :

## 👨‍💻 ผู้พัฒนา (Contributors)
- นายนันทกร แสวงจิตร Project Manager / CI-CD Integrator:
  setup repo, pipeline, project board
  Test Code ก่อน deploy ไปใช้งานจริง
  CI/CD ทำการรวมโค้ด Deploy Project ขึ้นเว็บไซต์ โดยใช้ render
- นายพชรพงศ์ สาหล่อน Automated Tester & QA:
  สร้าง Automated QA Checks , มีส่วนใน CI
  ทดสอบโปรแกรม test ระบบต่างๆ เช่น API 
  Feedback แจ้ง Bug หรือ Error ให้กับทีม
- นายเกียรติพงษ์ เผดิมศักดิ์ Project Manager / Core Developer :
  วางแผนและกำหนดขอบเขตของโครงงาน
  ออกแบบโครงสร้างระบบและการทำงานของ API
  เขียนโค้ดหลักของระบบ เช่น BMI Calculator, Main() และ Flask Self Made Mock API
