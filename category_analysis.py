# category_analytics.py

import ijson
from collections import defaultdict, Counter
from tqdm import tqdm
from pprint import pprint

TERM_CATEGORY_FILE = "data/term_category_backtrack.json"

print(f"📂 Streaming: {TERM_CATEGORY_FILE}")

# Initialize trackers
term_counter = Counter()
category_terms = defaultdict(list)
year_category_count = defaultdict(lambda: defaultdict(int))

# Estimate number of entries for tqdm bar
with open(TERM_CATEGORY_FILE, "r") as f:
    total = sum(1 for _ in ijson.items(f, 'item'))

with open(TERM_CATEGORY_FILE, "r") as f:
    parser = ijson.kvitems(f, '')  # Stream as key-value pairs

    for term, data in tqdm(parser, total=total, desc="🔍 Processing terms"):
        count = data.get("count", 0)
        category = data.get("category", "General/Other")
        references = data.get("references", [])

        term_counter[(term, category)] = count
        category_terms[category].append((term, count))

        for ref in references:
            year = ref.get("Year")
            if isinstance(year, int):
                year_category_count[year][category] += 1

# --- Functions ---

def top_n_terms(n=10):
    return sorted(term_counter.items(), key=lambda x: x[1], reverse=True)[:n]

def top_terms_per_category(n=5):
    result = {}
    for cat, terms in category_terms.items():
        result[cat] = sorted(terms, key=lambda x: x[1], reverse=True)[:n]
    return result

def get_yearwise_category_trends():
    return dict(year_category_count)

# --- Output Results ---

print("\n🎯 Top 10 Global Terms:")
for (term, category), count in top_n_terms():
    print(f"{term}: {count} [{category}]")

print("\n📚 Top Terms per Category:")
for category, terms in top_terms_per_category().items():
    print(f"\n{category}:")
    for term, count in terms:
        print(f"  {term}: {count}")

print("\n📈 Year-wise Category Trends:")
pprint(get_yearwise_category_trends())

print("\n✅ Category analysis completed.")
