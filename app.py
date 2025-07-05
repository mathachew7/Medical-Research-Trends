from flask import Flask, jsonify, send_from_directory, render_template, request
import pandas as pd
import os
import json
import ijson
from collections import Counter

app = Flask(__name__)

# --- Paths ---
DATA_DIR = "data"
CATEGORY_TRENDS_PATH = os.path.join(DATA_DIR, "category_trends.csv")
TERM_CATEGORY_BACKTRACK = os.path.join(DATA_DIR, "term_category_backtrack.json")

# Dashboard JSON files
DASHBOARD_STATS = os.path.join(DATA_DIR, "dashboard_stats.json")
FORECAST_DATA = os.path.join(DATA_DIR, "forecast_data.json")
TOP_KEYWORDS = os.path.join(DATA_DIR, "top_keywords_sparklines.json")
CO_OCCURRENCE = os.path.join(DATA_DIR, "keyword_co_occurrence.json")
RECENT_ABSTRACTS = os.path.join(DATA_DIR, "recent_abstracts.json")

# --- Load category trends ---
print("📊 Loading category trend data...")
try:
    trends_df = pd.read_csv(CATEGORY_TRENDS_PATH)
    trends_df['Year'] = trends_df['Year'].astype(int)
    print("✅ Loaded category_trends.csv")
except Exception as e:
    print("❌ Failed to load category_trends.csv:", e)
    trends_df = pd.DataFrame()

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/category_distribution')
def get_category_distribution():
    try:
        if trends_df.empty:
            return jsonify({"error": "Trend data not available"}), 500

        df = trends_df[trends_df["Year"] <= 2024]
        category_totals = df.drop(columns=["Year"]).sum().sort_values(ascending=False)

        result = [
            {"category": category, "count": int(count)}
            for category, count in category_totals.items()
        ]
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/trends')
def get_all_trends():
    if trends_df.empty:
        return jsonify({"error": "Trend data not available"}), 500
    filtered = trends_df[trends_df["Year"] <= 2024]
    return jsonify({"trends": filtered.to_dict(orient='records')})

@app.route('/top_terms')
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

@app.route('/references')
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

# --- Dashboard stats (fast from JSON) ---
@app.route('/stats')
def serve_dashboard_stats():
    try:
        with open(DASHBOARD_STATS) as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/forecast')
def serve_forecast_data():
    try:
        with open(FORECAST_DATA) as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/top_keywords')
def serve_top_keywords():
    try:
        with open(TOP_KEYWORDS) as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/co_occurrence')
def serve_co_occurrence():
    try:
        with open(CO_OCCURRENCE) as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/recent_abstracts')
def serve_recent_abstracts():
    try:
        with open(RECENT_ABSTRACTS) as f:
            data = json.load(f)
            filtered = [d for d in data if int(d.get("Year", 0)) <= 2024]
            return jsonify(filtered)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# --- Main ---
if __name__ == '__main__':
    print("\n🚀 Flask running at: http://127.0.0.1:5000/")
    app.run(debug=True)
