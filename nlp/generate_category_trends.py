import ijson
import pandas as pd
from collections import defaultdict
from tqdm import tqdm
import os

# --- Paths ---
TERM_JSON_PATH = "data/term_category_backtrack.json"
OUTPUT_CSV_PATH = "data/category_trends.csv"

# --- Prepare output directory ---
os.makedirs(os.path.dirname(OUTPUT_CSV_PATH), exist_ok=True)

# --- Count total items for tqdm (first pass) ---
print(f"📊 Counting total terms in: {TERM_JSON_PATH}")
try:
    with open(TERM_JSON_PATH, 'rb') as f:
        total_terms = sum(1 for _ in ijson.kvitems(f, ''))
    print(f"🔢 Total terms: {total_terms}")
except Exception as e:
    print(f"❌ Failed to count terms: {e}")
    total_terms = None

# --- Process file with streaming + progress bar ---
print(f"📂 Streaming terms with progress bar...")
category_year_counts = defaultdict(lambda: defaultdict(int))

try:
    with open(TERM_JSON_PATH, 'rb') as f:
        parser = ijson.kvitems(f, '')
        parser = tqdm(parser, total=total_terms, desc="Processing terms", unit="term")
        for term, entry in parser:
            category = entry.get("category", "General/Other")
            for ref in entry.get("references", []):
                year = ref.get("Year")
                if isinstance(year, int):
                    category_year_counts[category][year] += 1
except Exception as e:
    print(f"❌ Failed during processing: {e}")
    exit(1)

# --- Compile DataFrame ---
print("🧩 Structuring trend data...")
all_years = sorted({year for cat in category_year_counts.values() for year in cat})
data = {"Year": all_years}

for category in sorted(category_year_counts):
    data[category] = [category_year_counts[category].get(year, 0) for year in all_years]

df = pd.DataFrame(data)
df.to_csv(OUTPUT_CSV_PATH, index=False)

print(f"✅ Saved trend data to {OUTPUT_CSV_PATH}")
print(df.head())
