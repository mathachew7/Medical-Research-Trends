# generate_reference_map.py
import ijson
import json
from collections import defaultdict
from tqdm import tqdm

INPUT_PATH = "data/term_category_backtrack.json"
OUTPUT_PATH = "data/keyword_reference_map.json"

print(f"🔄 Streaming from: {INPUT_PATH}")
keyword_refs = defaultdict(list)

try:
    with open(INPUT_PATH, 'rb') as f:
        parser = ijson.kvitems(f, '')
        for term, meta in tqdm(parser, desc="Processing terms"):
            references = meta.get('references', [])
            for ref in references:
                keyword_refs[term].append({
                    "PMID": ref.get("PMID", ""),
                    "Year": ref.get("Year", ""),
                    "Link": ref.get("Link", "")
                })
except Exception as e:
    print(f"❌ Error: {e}")

print(f"💾 Saving to: {OUTPUT_PATH}")
with open(OUTPUT_PATH, "w") as out:
    json.dump(keyword_refs, out, indent=2)

print("✅ Reference map generated.")
