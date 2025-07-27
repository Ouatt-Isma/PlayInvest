import pandas as pd

# Load the Excel file (adjust the filename as needed)
df = pd.read_csv("articles_source.csv")

# Rename columns to match your DB schema
df.rename(columns={
    "Titre": "topic",
    "Objectif pédagogique": "pedagogical_objective",
    "Public visé": "audience",
    "Niveau de difficulté": "difficulty_level",
    "Catégorie PlayInvest": "category"
}, inplace=True)

# Add required fields
df["type"] = "article"
df["content"] = ""  # Placeholder for now, adjust if you have content

# Reorder columns to match the table insert order
df = df[[
    "topic",
    "type",
    "content",
    "pedagogical_objective",
    "audience",
    "difficulty_level",
    "category"
]]

# Save to CSV (UTF-8 encoding with quotes for special characters)
df.to_csv("articles_to_import.csv", index=False, encoding="utf-8", quoting=1)  # quoting=1 = csv.QUOTE_ALL
