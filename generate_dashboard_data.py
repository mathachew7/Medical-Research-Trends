import pandas as pd
import json
import os
import ijson
from collections import defaultdict, Counter

# --- Paths ---
DATA_DIR = "data"
TRENDS_CSV = os.path.join(DATA_DIR, "category_trends.csv")
BACKTRACK_JSON = os.path.join(DATA_DIR, "term_category_backtrack.json")

OUTPUT_STATS = os.path.join(DATA_DIR, "dashboard_stats.json")
OUTPUT_FORECAST = os.path.join(DATA_DIR, "forecast_data.json")
OUTPUT_TOP_KEYWORDS = os.path.join(DATA_DIR, "top_keywords_sparklines.json")
OUTPUT_CLOUD = os.path.join(DATA_DIR, "keyword_co_occurrence.json")
OUTPUT_RECENT = os.path.join(DATA_DIR, "recent_abstracts.json")

# --- Load trends ---
trends_df = pd.read_csv(TRENDS_CSV)
trends_df = trends_df[trends_df['Year'] <= 2024]
trends_df['Year'] = trends_df['Year'].astype(int)

# --- dashboard_stats.json ---
total_pubs = trends_df.drop(columns=['Year']).sum().sum()
category_totals = trends_df.drop(columns=['Year']).sum().to_dict()
top_category = max(category_totals, key=category_totals.get)

year_groups = trends_df.groupby('Year').sum()
years = sorted(year_groups.index)
growth_rates = {}
for cat in category_totals:
    y1 = year_groups[cat].get(years[-2], 0)
    y2 = year_groups[cat].get(years[-1], 0)
    if y1 > 0:
        growth = ((y2 - y1) / y1) * 100
        growth_rates[cat] = round(growth, 2)
max_growth_cat = max(growth_rates, key=growth_rates.get)

# --- Extract top terms per category with sparklines ---
category_term_map = defaultdict(list)
term_yearly_count = defaultdict(lambda: [0] * len(years))

with open(BACKTRACK_JSON, 'rb') as f:
    for term, meta in ijson.kvitems(f, ''):
        cat = meta.get("category", "General/Other")
        count = meta.get("count", 0)
        references = meta.get("references", [])

        # Skip if no refs or count
        if not references or count == 0:
            continue

        # Count per year
        year_counter = Counter(int(ref['Year']) for ref in references if ref.get("Year") and int(ref["Year"]) <= 2024)
        for idx, yr in enumerate(years):
            term_yearly_count[term][idx] = year_counter.get(yr, 0)

        category_term_map[cat].append({
            "term": term,
            "count": count,
            "sparkline": term_yearly_count[term]
        })

# Keep top 30 terms per category
category_keywords = []
for cat, terms in category_term_map.items():
    top_terms = sorted(terms, key=lambda x: x['count'], reverse=True)[:30]
    category_keywords.append({
        "category": cat,
        "keywords": top_terms
    })

# --- Save top_keywords_sparklines.json ---
with open(OUTPUT_TOP_KEYWORDS, 'w') as f:
    json.dump(category_keywords, f, indent=2)

# --- top keywords for top category into dashboard_stats.json ---
top_keywords = []
for c in category_keywords:
    if c["category"] == top_category:
        top_keywords = [{"term": k["term"], "count": k["count"]} for k in c["keywords"][:10]]
        break

dashboard_stats = {
    "total_publications": int(total_pubs),
    "top_category": top_category,
    "growth_rate": f"{growth_rates.get(top_category, 0.0):.2f}%",
    "growth_category": max_growth_cat,
    "category_growth": f"{growth_rates.get(max_growth_cat, 0.0):.2f}%",
    "top_keywords": top_keywords
}
with open(OUTPUT_STATS, 'w') as f:
    json.dump(dashboard_stats, f, indent=2)

# --- forecast_data.json ---
total_yearly = trends_df.drop(columns=['Year']).sum(axis=1)
recent = total_yearly.iloc[-3:]
growth = recent.pct_change().mean()
next_val = int(total_yearly.iloc[-1] * (1 + growth)) if pd.notna(growth) else int(total_yearly.iloc[-1])
forecast = {
    "years": [str(years[-1]), str(years[-1] + 1)],
    "counts": [int(total_yearly.iloc[-1]), next_val]
}
with open(OUTPUT_FORECAST, 'w') as f:
    json.dump(forecast, f, indent=2)

# --- keyword_co_occurrence.json ---
co_counter = Counter()
with open(BACKTRACK_JSON, 'rb') as f:
    for _, meta in ijson.kvitems(f, ''):
        co_terms = meta.get("co_occurrence", [])
        co_counter.update(co_terms)
co_data = {
    "terms": [term for term, _ in co_counter.most_common(50)]
}
with open(OUTPUT_CLOUD, 'w') as f:
    json.dump(co_data, f, indent=2)

# --- recent_abstracts.json ---
refs = []
with open(BACKTRACK_JSON, 'rb') as f:
    for term, meta in ijson.kvitems(f, ''):
        for ref in meta.get("references", []):
            year = ref.get("Year")
            pmid = ref.get("PMID")
            if year and pmid and int(year) <= 2024:
                refs.append({
                    "title": ref.get("title", term),
                    "Year": int(year),
                    "PMID": str(pmid)
                })
refs.sort(key=lambda x: x['Year'], reverse=True)
with open(OUTPUT_RECENT, 'w') as f:
    json.dump(refs[:10], f, indent=2)

print("✅ Dashboard data generated with category-wise top keywords and sparklines.")
