from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    salary = float(data.get("salary", 0))
    expenses = data.get("expenses", [])

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
    yearly_savings = monthly_savings * 12

    advice = generate_advice(
        salary, total, important_total,
        less_total, optional_total, monthly_savings
    )

    what_if = {
        "current": total,
        "skip_optional": important_total + less_total,
        "only_important": important_total
    }

    result = {
        "expenses": categorized,
        "important": important_total,
        "less": less_total,
        "optional": optional_total,
        "total": total,
        "monthly_savings": monthly_savings,
        "yearly_savings": yearly_savings,
        "advice": advice,
        "what_if": what_if
    }

    return jsonify(result)


def categorize_expense(name):
    important_keywords = [
        "rent", "house", "electricity", "electric", "bill", "water",
        "gas", "internet", "wifi", "medicine", "medical", "doctor",
        "hospital", "school", "fee", "tuition", "grocery", "groceries",
        "food", "kitchen", "transport", "fuel", "petrol", "diesel",
        "insurance", "loan", "emi", "debt", "tax"
    ]
    less_important_keywords = [
        "phone", "mobile", "sim", "data", "package", "subscription",
        "netflix", "spotify", "youtube", "prime", "gym", "fitness",
        "clothes", "shopping", "dining", "restaurant", "cafe",
        "coffee", "snacks", "cigarette", "beauty", "salon"
    ]
    optional_keywords = [
        "game", "gaming", "movie", "cinema", "party", "trip",
        "travel", "vacation", "gift", "donation", "luxury",
        "entertainment", "hobby", "toy", "alcohol", "bar"
    ]

    for kw in important_keywords:
        if kw in name:
            return "important"
    for kw in less_important_keywords:
        if kw in name:
            return "less_important"
    for kw in optional_keywords:
        if kw in name:
            return "optional"

    return "less_important"


def generate_advice(salary, total, important, less, optional, savings):
    advice = []

    if savings < 0:
        advice.append({
            "type": "danger",
            "text": f"You are overspending by Rs {abs(savings):,.0f} every month. "
                    f"Your expenses (Rs {total:,.0f}) exceed your salary (Rs {salary:,.0f}). "
                    f"Immediately cut optional and less important expenses."
        })
    elif savings < salary * 0.1:
        advice.append({
            "type": "warning",
            "text": f"Your savings are very low (Rs {savings:,.0f}). "
                    f"Try to save at least 20% of your salary for financial safety."
        })
    else:
        advice.append({
            "type": "success",
            "text": f"Great job! You are saving Rs {savings:,.0f} every month. "
                    f"Consider investing this in savings or mutual funds."
        })

    if optional > 0:
        advice.append({
            "type": "tip",
            "text": f"You can save Rs {optional:,.0f} per month by reducing optional "
                    f"expenses like entertainment and luxury items."
        })

    if less > salary * 0.2:
        advice.append({
            "type": "warning",
            "text": f"Your less important expenses are high (Rs {less:,.0f}). "
                    f"Review subscriptions and dining costs to cut them down."
        })

    if important > salary * 0.6:
        advice.append({
            "type": "danger",
            "text": f"Your essential expenses (Rs {important:,.0f}) take more than "
                    f"60% of your salary. Look for ways to reduce fixed costs."
        })

    return advice


if __name__ == "__main__":
    app.run(debug=True)