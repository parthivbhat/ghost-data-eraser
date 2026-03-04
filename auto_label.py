import pandas as pd

# Load dataset
df = pd.read_csv("email_dataset.csv")

positive_keywords = [
    "verify",
    "verification",
    "account created",
    "welcome",
    "otp",
    "one time password",
    "registration confirmation",
    "confirm your email",
    "password reset",
    "security alert",
    "new sign in"
]

df["Subject"] = df["Subject"].fillna("").str.lower()

df["Label"] = df["Subject"].apply(
    lambda x: 1 if any(keyword in x for keyword in positive_keywords) else 0
)

df.to_csv("email_dataset.csv", index=False)

print("Auto labeling completed successfully!")
