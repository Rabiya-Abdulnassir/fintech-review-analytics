import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/raw_reviews.csv")

print("Initial shape:", df.shape)

# Remove duplicates
df = df.drop_duplicates()

# Handle missing values
df = df.dropna(subset=["review", "rating"])

# Normalize date format
df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

# Keep required columns
df = df[["review", "rating", "date", "bank", "source"]]

print("Cleaned shape:", df.shape)

# Save cleaned dataset
df.to_csv("data/raw/cleaned_reviews.csv", index=False)

print("Preprocessing complete.")