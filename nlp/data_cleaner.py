# data_cleaner.py

import os
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm

# --- Setup ---
nltk.download('stopwords')
nltk.download('wordnet')
tqdm.pandas()

RAW_PATH = "data/pubmed_abstracts_raw.csv"
CLEANED_PATH = "data/pubmed_abstracts_processed.csv"
MIN_YEAR = 2015

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', str(text).lower())
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words and len(t) > 2]
    return ' '.join(tokens)

def clean_data(df):
    df.dropna(subset=['PMID'], inplace=True)
    df.drop_duplicates(subset='PMID', inplace=True)
    df['PublicationYear'] = pd.to_numeric(df['PublicationYear'], errors='coerce')
    df = df[df['PublicationYear'] >= MIN_YEAR].copy()
    df['Abstract'] = df['Abstract'].fillna('')
    df['Title'] = df['Title'].fillna('')
    df['FullText'] = df['Title'] + ' ' + df['Abstract']
    df['CleanText'] = df['FullText'].progress_apply(clean_text)
    df = df[df['CleanText'].str.strip() != '']
    return df

if __name__ == "__main__":
    print("🔹 Loading raw data...")
    df = pd.read_csv(RAW_PATH)
    df_clean = clean_data(df)
    df_clean.to_csv(CLEANED_PATH, index=False)
    print(f"✅ Cleaned data saved to {CLEANED_PATH}. Shape: {df_clean.shape}")
