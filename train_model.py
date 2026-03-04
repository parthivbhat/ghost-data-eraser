import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report

# -------------------------------------------------
# 1. Load Dataset
# -------------------------------------------------

print("Loading dataset...")
df = pd.read_csv("email_dataset.csv")

# Remove rows with missing Subject or Label
df = df.dropna(subset=["Subject", "Label"])

# Ensure label is integer
df["Label"] = df["Label"].astype(int)

print("Total samples:", len(df))
print("Class distribution:\n", df["Label"].value_counts())

# -------------------------------------------------
# 2. Train-Test Split
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    df["Subject"],
    df["Label"],
    test_size=0.2,
    random_state=42,
    stratify=df["Label"]
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# -------------------------------------------------
# 3. TF-IDF Vectorization
# -------------------------------------------------

vectorizer = TfidfVectorizer(
    stop_words='english',
    max_features=3000
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# -------------------------------------------------
# 4. Train Model
# -------------------------------------------------

model = LogisticRegression(class_weight="balanced")
model.fit(X_train_tfidf, y_train)

# -------------------------------------------------
# 5. Evaluation
# -------------------------------------------------

y_pred = model.predict(X_test_tfidf)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# -------------------------------------------------
# 6. Save Model + Vectorizer
# -------------------------------------------------

joblib.dump(model, "signup_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\n✅ Model and vectorizer saved successfully!")
