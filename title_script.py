import json
import os

# ✅ 1. Adjust this to the correct path where your JSON files are
folder_path = os.path.join(os.getcwd(), 'json')  # or use absolute path

# ✅ 2. Generate file list
file_names = [f"{i:03}.json" for i in range(1, 16)]  # 001.json to 015.json

# ✅ 3. Initialize title_number
title_number = 1

# ✅ 4. Loop over all files
for file_name in file_names:
    full_path = os.path.join(folder_path, file_name)
    print(f"Processing {full_path}")

    if not os.path.isfile(full_path):
        print(f"❌ File not found: {full_path}")
        continue

    # Load JSON
    with open(full_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Add title_number to each chapter
    for chapter in data:
        chapter['title_number'] = title_number
        title_number += 1

    # Save back to same file (or change filename if you want to preserve original)
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ All titles numbered successfully.")
