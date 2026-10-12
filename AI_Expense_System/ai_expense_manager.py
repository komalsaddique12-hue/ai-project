# ai_expense_manager.py
import pickle
import numpy as np
from sklearn.linear_model import LinearRegression

# ---------- Load AI Model ----------
with open("expense_model.pkl", "rb") as f:
    ai_model = pickle.load(f)

# ---------- AI Categorization Function ----------
def categorize(expense_name):
    return ai_model.predict([expense_name.lower()])[0]

# ---------- Welcome ----------
print("=" * 55)
print("🤖 AI Salary & Expense Manager")
print("=" * 55)

# ---------- User Input ----------
salary = float(input("💰 Apni monthly salary enter karein: "))
n = int(input("📝 Kitne expenses hain? "))

expenses = []
for i in range(n):
    print(f"\n--- Expense {i+1} ---")
    name = input("  Expense ka naam: ")
    amount = float(input(f"  {name} ki amount: "))
    cat = categorize(name)   # 🤖 AI decide karega
    expenses.append({"name": name, "amount": amount, "category": cat})
    print(f"  🤖 AI ne categorize kiya: {cat}")

# ---------- Totals ----------
important = sum(e["amount"] for e in expenses if e["category"] == "important")
less = sum(e["amount"] for e in expenses if e["category"] == "less_important")
optional = sum(e["amount"] for e in expenses if e["category"] == "optional")
total = important + less + optional
monthly_savings = salary - total

# ---------- AI Savings Predictor (12 months) ----------
X_train = np.array([[1, 40000], [2, 42000], [3, 45000],
                    [4, 43000], [5, 47000], [6, 46000]])
y_train = np.array([20000, 18000, 15000, 17000, 13000, 14000])

predictor = LinearRegression()
predictor.fit(X_train, y_train)

future_X = np.array([[m, total] for m in range(7, 19)])
future_savings = predictor.predict(future_X)
yearly_savings = future_savings.sum()

# ---------- Report ----------
print("\n" + "=" * 55)
print("📊 AI EXPENSE REPORT")
print("=" * 55)

for e in expenses:
    emoji = {"important": "🔴", "less_important": "🟡", "optional": "🟢"}[e["category"]]
    print(f"{emoji} {e['name']:15} Rs {e['amount']:>8.0f}  → {e['category']}")

print("-" * 55)
print(f"🔴 Important Total   : Rs {important:.0f}")
print(f"🟡 Less Important    : Rs {less:.0f}")
print(f"🟢 Optional Total    : Rs {optional:.0f}")
print(f"💸 Total Expenses    : Rs {total:.0f}")
print(f"💰 Monthly Savings   : Rs {monthly_savings:.0f}")
print(f"📅 Yearly Savings    : Rs {round(yearly_savings)}")

# ---------- AI Advisor ----------
print("\n" + "=" * 55)
print("🧠 AI ADVISOR - Suggestions")
print("=" * 55)

if monthly_savings < 0:
    print("⚠️ Aap loss mein hain!")
    print(f"   👉 Optional expenses (Rs {optional:.0f}) turant kam karein.")
    print(f"   👉 Less important (Rs {less:.0f}) mein 30% cut karein.")
    print(f"   💡 Bachat possible: Rs {optional + less*0.3:.0f}/month")
elif monthly_savings < salary * 0.2:
    print("⚠️ Savings 20% se kam hai (50-30-20 rule).")
    print(f"   👉 Optional Rs {optional:.0f} → 50% kam karein.")
    print(f"   💡 Extra bachat: Rs {optional*0.5:.0f}/month")
else:
    print("✅ Excellent! Aap 20%+ save kar rahe hain.")
    print(f"   👉 Optional (Rs {optional:.0f}) ko invest karein — mutual funds/stocks.")

# ---------- What-If Analysis ----------
print("\n" + "=" * 55)
print("🔮 WHAT-IF ANALYSIS")
print("=" * 55)
print(f"Current plan          : Rs {monthly_savings:.0f}/month")
print(f"Optional skip karne se: Rs {salary - important - less:.0f}/month")
print(f"Sirf Important rakhein: Rs {salary - important:.0f}/month")