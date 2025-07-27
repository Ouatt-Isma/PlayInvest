import os
import pandas as pd

# Load the CSV file
csv_path = 'articles_to_imp.csv'  # Change this if needed
df = pd.read_csv(csv_path)

# Loop through each row in the CSV
for _, row in df.iterrows():
    raw_topic = row['Titre']
    topic = raw_topic.replace(':', '_').replace('\'', '_').replace('?', '_')
    article_id = row['article_id']
    
    folder_path = os.path.join('.', topic)  # Folder name = topic
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        continue

    # List files in the folder (we assume only one relevant file per article)
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Skip if not a file
        if not os.path.isfile(file_path):
            continue

        # Get file extension
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        # New filename: article_id + extension
        new_filename = f"{article_id}{ext}"
        new_file_path = os.path.join(folder_path, new_filename)

        # Rename the file
        os.rename(file_path, new_file_path)
        print(f"Renamed: {file_path} → {new_file_path}")
