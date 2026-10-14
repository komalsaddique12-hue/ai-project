from flask import Flask, render_template, request, jsonify
import pickle
import os

app = Flask(__name__)

# ---------- Load AI Model (Safe Path for Vercel) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "expense_model.pkl")

try:
    with open(MODEL_PATH, "rb") as f:
        ai_model = pickle.load(f)
    print("✅ AI Model loaded successfully")
except Exception as e:
    print("❌ MODEL LOAD ERROR:", e)
    ai_model = None


# ---------- AI Categorization ----------
def categorize_expense(name):
    if ai_model is None:
        # Fallback: keyword-based categorization if model fails
        name = name.lower()
        important_kw = ["rent", "house", "bill", "gas", "water", "electric",
                        "medical", "doctor", "medicine", "school", "fee",
                        "grocery", "khana", "transport", "emi", "loan", "insurance"]
        less_kw = ["internet", "wifi", "mobile", "phone", "clothing", "kapray",
                   "restaurant", "gym", "netflix", "subscription", "shopping"]
        optional_kw = ["movie", "cinema", "travel", "trip", "game", "gift", "luxury"]

        for kw in important_kw:
            if kw in name: return "important"
        for kw in less_kw:
            if kw in name: return "less_important"
        for kw in optional_kw:
            if kw in name: return "optional"
        return "less_important"

    try:
        return ai_model.predict([name.lower()])[0]
    except Exception as e:
        print("AI Predict Error:", e)
        return "less_important"


# ---------- Analyze Single Month ----------
def analyze_month(salary, expenses):
    categorized = []
    important_total = 0
    less_total = 0
    optional_total = 0

    for exp in expenses:
        name = exp["name"].strip().lower()
        amount = float(exp["amount"])
        category = categorize_expense(name)

        categorized.append({
            "name": exp["name"],
            "amount": amount,
            "category": category
        })

        if category == "important":
            important_total += amount
        elif category == "less_important":
            less_total += amount
        else:
            optional_total += amount

    total = important_total + less_total + optional_total
    monthly_savings = salary - total

    return {
        "expenses": categorized,
        "important": important_total,
        "less": less_total,
        "optional": optional_total,
        "total": total,
        "monthly_savings": monthly_savings
    }


# ---------- Comparison Advice ----------
def generate_comparison_advice(prev, curr, prev_salary, curr_salary):
    advice = []

    prev_savings = prev_salary - prev["total"]
    curr_savings = curr_salary - curr["total"]
    diff = curr_savings - prev_savings
    diff_pct = (diff / abs(prev_savings) * 100) if prev_savings != 0 else 0

    if diff > 0:
        advice.append({
            "type": "success",
            "text": f"Great! Your savings increased by Rs {diff:,.0f} ({diff_pct:+.1f}%) compared to last month."
        })
    elif diff < 0:
        advice.append({
            "type": "danger",
            "text": f"⚠ Alert: Your savings decreased by Rs {abs(diff):,.0f} ({diff_pct:.1f}%) compared to last month."
        })
    else:
        advice.append({
            "type": "tip",
            "text": "Your savings are same as last month. Try to push a bit more this month."
        })

    exp_diff = curr["total"] - prev["total"]
    if exp_diff > 0:
        advice.append({
            "type": "warning",
            "text": f"Your expenses increased by Rs {exp_diff:,.0f} this month. Review your spending."
        })
    elif exp_diff < 0:
        advice.append({
            "type": "success",
            "text": f"Nice! You reduced expenses by Rs {abs(exp_diff):,.0f} this month. Keep it up."
        })

    if curr["optional"] > 0:
        advice.append({
            "type": "tip",
            "text": f"You can save Rs {curr['optional']:,.0f} more by cutting optional expenses."
        })

    if curr["total"] > 0 and curr["important"] / curr["total"] > 0.7:
        advice.append({
            "type": "warning",
            "text": f"Essentials take {curr['important']/curr['total']*100:.0f}% of your expenses. Try reducing fixed costs."
        })

    curr_rate = (curr_savings / curr_salary * 100) if curr_salary > 0 else 0
    if curr_rate < 10:
        advice.append({
            "type": "danger",
            "text": f"Your current savings rate is only {curr_rate:.1f}%. Aim for at least 20%."
        })
    elif curr_rate >= 20:
        advice.append({
            "type": "success",
            "text": f"Excellent! You're saving {curr_rate:.1f}% of your income. Consider investing the surplus."
        })

    return advice


# ---------- Routes ----------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    prev_data = data.get("previous", {})
    curr_data = data.get("current", {})

    prev_salary = float(prev_data.get("salary", 0))
    curr_salary = float(curr_data.get("salary", 0))

    prev_expenses = prev_data.get("expenses", [])
    curr_expenses = curr_data.get("expenses", [])

    prev_result = analyze_month(prev_salary, prev_expenses)
    curr_result = analyze_month(curr_salary, curr_expenses)

    advice = generate_comparison_advice(
        prev_result, curr_result, prev_salary, curr_salary
    )

    result = {
        "previous": prev_result,
        "current": curr_result,
        "advice": advice
    }

    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)