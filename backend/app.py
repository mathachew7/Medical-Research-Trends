from flask import Flask, jsonify, request
import pandas as pd
import json
import ijson
import os
from flask_cors import CORS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")

# File paths
CATEGORY_TRENDS_PATH = os.path.join(DATA_DIR, "category_trends.csv")
TERM_CATEGORY_BACKTRACK = os.path.join(DATA_DIR, "term_category_backtrack.json")
DASHBOARD_STATS = os.path.join(DATA_DIR, "dashboard_stats.json")
FORECAST_DATA = os.path.join(DATA_DIR, "forecast_data.json")
TOP_KEYWORDS = os.path.join(DATA_DIR, "top_keywords_sparklines.json")
CO_OCCURRENCE = os.path.join(DATA_DIR, "keyword_co_occurrence.json")
RECENT_ABSTRACTS = os.path.join(DATA_DIR, "recent_abstracts.json")

# Init Flask
app = Flask(__name__)
CORS(app)

# Load trend data once
print("📊 Loading category trend data...")
try:
    trends_df = pd.read_csv(CATEGORY_TRENDS_PATH)
    trends_df['Year'] = trends_df['Year'].astype(int)
    print("✅ Loaded category_trends.csv")
except Exception as e:
    print("❌ Failed to load category_trends.csv:", e)
    trends_df = pd.DataFrame()


@app.route('/api/category_distribution')
def get_category_distribution():
    if trends_df.empty:
        return jsonify({"error": "Trend data not available"}), 500

    df = trends_df[trends_df["Year"] <= 2024]
    category_totals = df.drop(columns=["Year"]).sum().sort_values(ascending=False)

    result = [
        {"category": category, "count": int(count)}
        for category, count in category_totals.items()
    ]
    return jsonify(result)


@app.route('/api/trends')
def get_all_trends():
    if trends_df.empty:
        return jsonify({"error": "Trend data not available"}), 500
    filtered = trends_df[trends_df["Year"] <= 2024]
    return jsonify({"trends": filtered.to_dict(orient='records')})


@app.route('/api/top_terms')
def get_top_terms():
    category = request.args.get("category", "").strip()
    N = int(request.args.get("top_n", 10))
    results = []

    try:
        term_counts = []
        with open(TERM_CATEGORY_BACKTRACK, 'rb') as f:
            for term, meta in ijson.kvitems(f, ''):
                term_cat = meta.get("category", "General/Other")
                if category and term_cat != category:
                    continue
                term_counts.append((term, meta))

        top_terms = sorted(term_counts, key=lambda x: x[1].get("count", 0), reverse=True)[:N]

        for term, meta in top_terms:
            results.append({
                "term": term,
                "count": meta.get("count", 0),
                "category": meta.get("category", "General/Other"),
                "references": meta.get("references", [])[:10]
            })

        return jsonify(results)

    except Exception as e:
        print("❌ Failed during top_terms:", e)
        return jsonify({"error": "Server error"}), 500


@app.route('/api/references')
def get_references():
    keyword = request.args.get("keyword", "").strip()
    if not keyword:
        return jsonify({"error": "No keyword provided"}), 400

    try:
        with open(TERM_CATEGORY_BACKTRACK, 'rb') as f:
            for term, data in ijson.kvitems(f, ''):
                if term == keyword:
                    refs = data.get("references", [])[:10]
                    references = [
                        {
                            "PMID": ref.get("PMID"),
                            "Year": ref.get("Year"),
                            "link": f"https://pubmed.ncbi.nlm.nih.gov/{ref.get('PMID')}/"
                        }
                        for ref in refs if ref.get("PMID")
                    ]
                    return jsonify({"keyword": keyword, "references": references})
        return jsonify({"keyword": keyword, "references": []})
    except Exception as e:
        print("❌ Failed to get references:", e)
        return jsonify({"error": "Server error"}), 500


@app.route('/api/stats')
def serve_dashboard_stats():
    try:
        with open(DASHBOARD_STATS) as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/forecast')
def serve_forecast_data():
    try:
        with open(FORECAST_DATA) as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/top_keywords')
def serve_top_keywords():
    try:
        with open(TOP_KEYWORDS) as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/co_occurrence')
def serve_co_occurrence():
    try:
        with open(CO_OCCURRENCE) as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/recent_abstracts')
def serve_recent_abstracts():
    try:
        with open(RECENT_ABSTRACTS) as f:
            data = json.load(f)
            filtered = [d for d in data if int(d.get("Year", 0)) <= 2024]
            return jsonify(filtered)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("\n🚀 API running at: http://127.0.0.1:5000/api/")
    app.run(debug=True)
