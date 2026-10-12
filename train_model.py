# train_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle

# Training Data — AI isse seekhega
data = {
    "expense": [
        "rent", "house rent", "bijli bill", "gas bill", "pani bill",
        "grocery", "khana", "medical", "doctor", "medicine",
        "school fee", "education", "tuition", "transport", "office bus",
        "emi", "loan", "installment",
        "internet", "wifi", "mobile bill", "clothing", "kapray",
        "eating out", "restaurant", "gym", "netflix", "subscription",
        "entertainment", "movie", "cinema", "shopping", "luxury",
        "gifts", "travel", "trip", "hobbies", "games"
    ],
    "category": [
        "important", "important", "important", "important", "important",
        "important", "important", "important", "important", "important",
        "important", "important", "important", "important", "important",
        "important", "important", "important",
        "less_important", "less_important", "less_important",
        "less_important", "less_important",
        "less_important", "less_important", "less_important",
        "less_important", "less_important",
        "optional", "optional", "optional", "optional", "optional",
        "optional", "optional", "optional", "optional", "optional"
    ]
}

df = pd.DataFrame(data)

# AI Pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB())
])

model.fit(df["expense"], df["category"])

# Save model
with open("expense_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ AI Model trained & saved as expense_model.pkl!")