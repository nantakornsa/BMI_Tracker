from flask import Flask, request, jsonify

app = Flask(__name__)

nutrition_data = {
    "underweight": ["chicken breast", "eggs", "nuts"],
    "normal": ["balanced meal with rice, veggies, protein"],
    "overweight": ["steamed vegetables", "salad", "lean protein"],
}


@app.route("/nutrition/<bmi_category>", methods=["GET"])
def get_nutrition(bmi_category):
    foods = nutrition_data.get(bmi_category, [])
    return jsonify({"foods": foods})


@app.route("/nutrition", methods=["POST"])
def post_nutrition():
    data = request.json
    bmi = data.get("bmi")
    if bmi < 18.5:
        category = "underweight"
    elif bmi < 25:
        category = "normal"
    else:
        category = "overweight"
    return jsonify({"foods": nutrition_data[category]})


if __name__ == "__main__":
    app.run(port=5000)
