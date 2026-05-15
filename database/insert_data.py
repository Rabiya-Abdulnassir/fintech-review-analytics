import pandas as pd
import psycopg2
from db_config import DB_CONFIG
from pathlib import Path

# -----------------------------
# LOAD DATA
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
csv_path = PROJECT_ROOT / "notebooks" / "data" / "processed" / "task2_final_output.csv"

df = pd.read_csv(csv_path)

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# -----------------------------
# RENAME COLUMNS
# -----------------------------
df = df.rename(columns={
    "bank": "bank_name",
    "review": "review_text"
})

print("Columns:", df.columns)
print("Sample data:\n", df.head())

# -----------------------------
# ENSURE bank_name EXISTS
# -----------------------------
if "bank_name" not in df.columns:
    raise ValueError("Dataset missing 'bank_name' column.")

# -----------------------------
# NORMALIZE BANK VALUES
# -----------------------------
df["bank_name"] = df["bank_name"].astype(str).str.strip().str.upper()

# -----------------------------
# CONNECT TO DB
# -----------------------------
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# -----------------------------
# FETCH BANK IDS
# -----------------------------
cur.execute("SELECT bank_id, bank_name FROM banks;")
rows = cur.fetchall()

bank_id_map = {
    name.strip().upper(): bank_id
    for bank_id, name in rows
}

print("Bank mapping:", bank_id_map)

# -----------------------------
# INSERT QUERY
# -----------------------------
insert_query = """
INSERT INTO reviews (
    bank_id,
    review_text,
    rating,
    review_date,
    sentiment_label,
    sentiment_score,
    identified_theme,
    source
)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
"""

# -----------------------------
# INSERT LOOP
# -----------------------------
inserted = 0
skipped = 0

for _, row in df.iterrows():

    bank_name = row["bank_name"]

    if bank_name not in bank_id_map:
        print(f"Skipping unknown bank: {bank_name}")
        skipped += 1
        continue

    review_text = row.get("review_text")

    # Skip empty reviews
    if pd.isna(review_text) or str(review_text).strip() == "":
        print("Skipping empty review")
        skipped += 1
        continue

    try:
        cur.execute(insert_query, (
            bank_id_map[bank_name],
            review_text,
            row.get("rating"),
            row.get("review_date"),
            row.get("sentiment_label"),
            row.get("sentiment_score"),
            row.get("identified_theme"),
            row.get("source", "Google Play")
        ))

        inserted += 1

    except Exception as e:
        print("Error inserting row:", e)
        skipped += 1

# -----------------------------
# COMMIT & CLOSE
# -----------------------------
conn.commit()
cur.close()
conn.close()

print("\n===== SUMMARY =====")
print("Inserted:", inserted)
print("Skipped:", skipped)