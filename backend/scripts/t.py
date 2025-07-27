import pandas as pd
import json
import csv

# Load CSV
df = pd.read_csv("your_file.csv")

# Rename the unnamed column
df.rename(columns={
    df.columns[0]: "module",  # usually "Unnamed: 0"
    "Thème": "topic",         # if needed
    "Question": "question",
    "Bonne réponse": "correct_answer"
}, inplace=True)

# Convert options A–D to JSON
df["options"] = df.apply(lambda row: json.dumps({
    "A": row["A"].strip(),
    "B": row["B"].strip(),
    "C": row["C"].strip(),
    "D": row["D"].strip()
}, ensure_ascii=False), axis=1)

# Drop original A–D columns
df.drop(columns=["A", "B", "C", "D"], inplace=True)

# Save with ; delimiter and quoting
df.to_csv("quizzes_transformed.csv", index=False, sep=';', quoting=csv.QUOTE_ALL, encoding='utf-8')
