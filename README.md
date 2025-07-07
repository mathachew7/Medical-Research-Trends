# MedResearchTrendSpotter | Medical-Research-Trends

An NLP-driven tool to identify and visualize trends in medical research from PubMed abstracts.

## Overview

The **MedResearchTrendSpotter** is a Python-based project designed to identify and visualize emerging trends in medical research. It automates the collection of PubMed abstracts, performs natural language processing (NLP) to extract key concepts (unigrams and bigrams), and analyzes their frequency over time.

This tool visualizes trends in PubMed abstracts (2015–2024) using NLP. Built to help researchers, educators, and policymakers understand what’s changing in medical research.

---

## Features

* **PubMed Data Collection** via Entrez API
* **Robust Preprocessing** with lemmatization and stopword removal
* **TF-IDF-based Keyword Extraction** (top 500 n-grams)
* **Trend & Category Analysis** with CSV + JSON output
* **SHAP + SciSpacy + Word Cloud (via dashboard)**
* **Interactive Dashboard:** Category-level trends, keyword growth, donut chart, and abstract references

---

## Project Structure

```bash
MedResearchTrendSpotter/
├── app.py                         # Flask server for dashboard
├── data_collector.py             # PubMed data fetcher
├── data_cleaner.py               # Raw cleaning pipeline
├── nlp_processor.py              # NLP processor + TF-IDF trends
├── category_analysis.py          # Assigns categories to keywords
├── generate_reference_map.py     # Maps keywords to abstract PMIDs
├── generate_dashboard_data.py    # Prepares JSON for dashboard
├── trend_visualizer.py           # Graph generator (optional)
│
├── data/
│   ├── pubmed_abstracts_raw.csv
│   ├── pubmed_abstracts_processed.csv
│   ├── abstract_keyword_backtrack.csv
│   ├── keyword_reference_map.json
│   ├── term_category_backtrack.json
│   ├── pmid_metadata_map.json
│   ├── dashboard_stats.json
│   ├── forecast_data.json
│   ├── recent_abstracts.json
│   ├── category_trends.csv
│   ├── top_keywords_sparklines.json
│   └── keyword_co_occurrence.json
│
├── templates/
│   └── index.html                # Dashboard UI
├── static/
│   ├── script.js                # Dashboard logic
│   └── style.css
├── logs/
│   └── extraction_log.txt
├── en_core_sci_lg-0.5.4.tar.gz   # SciSpacy model
├── requirements.txt
├── README.md
└── test.py
```

---

## How It Works: Problem → Process → Product

### 🎯 Problem

Medical researchers want to understand what’s trending in their field, but reading through thousands of abstracts is overwhelming.

### 🧠 Process

We:

* Pulled 62,000+ abstracts from PubMed
* Cleaned and lemmatized them
* Extracted 1-2 word medical phrases using TF-IDF
* Mapped them to categories
* Analyzed growth and patterns
* Built an interactive dashboard

### 📊 Product (What You See)

An interactive web dashboard that:

* Shows top trending categories
* Visualizes keyword usage over time
* Highlights fast-growing categories
* Shows related PMIDs + abstract links

---

## 🔧 Setup Instructions

### Prerequisites

* Python 3.8+
* Git
* NCBI API Key (free)

### Installation

```bash
git clone https://github.com/mathachew7/MedResearchTrendSpotter.git
cd MedResearchTrendSpotter
python -m venv venv
source venv/bin/activate        # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
```

### NLTK Data Setup

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
```

### SciSpacy Model

```bash
pip install en-core-sci-lg --no-deps
pip install ./en_core_sci_lg-0.5.4.tar.gz
```

### .env File Setup

Create `.env` with:

```
NCBI_API_KEY=YOUR_API_KEY
NCBI_EMAIL=your@email.com
```

---

## 🧪 Run the Pipeline (Step-by-Step)

### Step 1: Fetch Abstracts from PubMed

```bash
python data_collector.py
```

### Step 2: Clean Abstracts

```bash
python data_cleaner.py
```

### Step 3: NLP + TF-IDF + Frequency Trends

```bash
python nlp_processor.py
```

### Step 4: Category Assignment

```bash
python category_analysis.py
```

### Step 5: Map Keywords to PMIDs

```bash
python generate_reference_map.py
```

### Step 6: Generate Dashboard Data

```bash
python generate_dashboard_data.py
```

### Step 7: Launch Dashboard

```bash
python app.py
```

Go to: [http://localhost:5000](http://localhost:5000)

---

## 📂 Outputs & Data Files

### CSVs:

* `pubmed_abstracts_raw.csv`
* `pubmed_abstracts_processed.csv`
* `category_trends.csv`
* `abstract_keyword_backtrack.csv`

### JSONs:

* `dashboard_stats.json`
* `forecast_data.json`
* `recent_abstracts.json`
* `term_category_backtrack.json`
* `keyword_reference_map.json`
* `keyword_co_occurrence.json`

### Other:

* `plots/*.png` – Trend screenshots
* `logs/extraction_log.txt`

---

## 📊 Dashboard Features

* 📈 Category Trend Lines
* 🍩 Donut Chart by Category (Latest Year)
* 🔥 Top Category + Growth Rate
* 🧬 Co-occurrence Cloud
* 🔗 Clickable Abstract References (PMIDs)

---

## 📜 License

MIT License

---

## 📬 Contact

For research collaborations or NIW reference:
**Subash Yadav**
📧 [subashyadav7@outlook.com](mailto:subashyadav7@outlook.com)
🔗 [LinkedIn](https://www.linkedin.com/in/mathachew7)

---
