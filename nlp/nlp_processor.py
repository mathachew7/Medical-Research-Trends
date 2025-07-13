import os
import pandas as pd
import spacy
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm
import logging
import json

# Setup directories
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)
logging.basicConfig(filename='logs/extraction_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load SciSpacy Biomedical Model
try:
    nlp = spacy.load("en_core_sci_lg")
    print("✅ Loaded SciSpacy biomedical model 'en_core_sci_lg'.")
except OSError:
    print("❌ Model not found. Install it with:")
    print("python -m pip install https://huggingface.co/allenai/scispacy/releases/download/v0.5.2/en_core_sci_lg-0.5.2.tar.gz")
    exit()

# Load processed abstract data
df = pd.read_csv("data/pubmed_abstracts_processed.csv")
print("📑 Columns in processed file:", df.columns.tolist())

# Validate necessary columns
required_cols = ['PMID', 'PublicationYear', 'Abstract', 'CleanText']
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"❌ Required column '{col}' not found in dataset.")

df['Abstract'] = df['Abstract'].fillna('').astype(str)
df['CleanText'] = df['CleanText'].fillna('').astype(str)
df['PublicationYear'] = pd.to_numeric(df['PublicationYear'], errors='coerce').astype(int)


#df = df.head(999)  # Limit for testing

# Extract medical terms
tqdm.pandas()

def extract_all_terms(row):
    idx = row.name
    text = row['CleanText']
    pmid = row['PMID']
    doc = nlp(text)
    terms = [ent.text.lower().strip() for ent in doc.ents if ent.text.strip()]
    unique_terms = sorted(set(terms))
    logging.info(f"Index {idx} | PMID: {pmid} | Terms: {unique_terms}")
    return " ".join(unique_terms)

print("🔍 Extracting biomedical terms...")
df['medical_terms'] = df.progress_apply(extract_all_terms, axis=1)
df = df[df['medical_terms'].str.strip() != '']
print(f"✅ Extracted medical terms for {len(df)} abstracts.")

# Save abstract-level mapping
df['PubMed_Link'] = df['PMID'].apply(lambda x: f"https://pubmed.ncbi.nlm.nih.gov/{x}")
df[['PMID', 'PublicationYear', 'Abstract', 'medical_terms', 'PubMed_Link']].to_csv("data/abstract_keyword_backtrack.csv", index=False)
print("✅ Saved abstract-level keywords to data/abstract_keyword_backtrack.csv")

# Save PMID-to-Year+Abstract Map
pmid_map = {}
for _, row in df.iterrows():
    pmid_map[str(row['PMID'])] = {
        "Year": int(row['PublicationYear']),
        "Abstract": row['Abstract']
    }
with open("data/pmid_metadata_map.json", "w") as f:
    json.dump(pmid_map, f, indent=2)
print("🗂️ Saved PMID to Year+Abstract mapping to data/pmid_metadata_map.json")

# Category mapping
CATEGORY_MAP = {
    "Oncology": ["cancer", "tumor", "carcinoma", "leukemia"],
    "Cardiology": ["cardiac", "heart", "angioplasty", "arrhythmia"],
    "Neurology": ["neuron", "brain", "stroke", "epilepsy"],
    "AI Methods": ["ai", "artificial intelligence", "machine learning", "deep learning"],
    "COVID/Post-pandemic": ["covid", "coronavirus", "vaccine", "pandemic"],
    "Genetic therapies": ["gene", "crispr", "genome editing", "genetic"],
    "Wearables / IoT": ["wearable", "iot", "sensor"],
    "Immunology": ["immune", "immunotherapy", "antibody"],
    "Diagnostics": ["diagnosis", "screening", "imaging"],
    "General/Other": ["cell", "therapy", "patient", "analysis", "clinical"]
}

# Reverse map: term -> category
TERM_TO_CATEGORY = {}
for category, terms in CATEGORY_MAP.items():
    for term in terms:
        TERM_TO_CATEGORY[term.lower()] = category

# Build term dictionary with simplified references
term_dict = defaultdict(lambda: {"category": None, "count": 0, "references": []})

for _, row in df.iterrows():
    pmid = row['PMID']
    year = int(row['PublicationYear'])
    abstract = row['Abstract']
    for term in row['medical_terms'].split():
        category = TERM_TO_CATEGORY.get(term, "General/Other")
        term_dict[term]["category"] = category
        term_dict[term]["count"] += 1
        term_dict[term]["references"].append({
            "PMID": pmid,
            "Year": year,
            "Abstract": abstract
        })

# Save full mapping
with open("data/term_category_backtrack.json", "w") as f:
    json.dump(term_dict, f, indent=2)

print("✅ Saved term-to-category mapping with counts and reference metadata to data/term_category_backtrack.json")
