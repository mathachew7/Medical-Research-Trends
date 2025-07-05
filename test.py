import json
import os

# Path to JSON file
file_path = os.path.join("data", "term_category_backtrack.json")

# Load the JSON data
with open(file_path, "r") as f:
    term_data = json.load(f)

print("\n🧠 Sample Categorized Terms with Reference Count:\n")

sampled = 0
for term, entry in term_data.items():
    count = entry.get("count", 0)
    category = entry.get("category", "Uncategorized")
    references = entry.get("references", [])

    if not references:
        continue

    sample_pmid = references[0] if isinstance(references[0], str) else references[0].get("PMID", "N/A")
    
    print(f"🔹 Term: {term}")
    print(f"   📂 Category: {category}")
    print(f"   🔢 Count: {count}")
    print(f"   📄 Sample PMID: {sample_pmid}\n")

    sampled += 1
    if sampled == 5:
        break
