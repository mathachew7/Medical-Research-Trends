import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
# NEW IMPORT: CountVectorizer for direct term frequency counting
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer 
from tqdm import tqdm # For progress bar

# --- NLTK Data Downloads (Run these in your terminal ONCE if you haven't) ---
# If you run the script and get an NLTK lookup error, uncomment and run:
# python -c "import nltk; nltk.download('stopwords')"
# python -c "import nltk; nltk.download('wordnet')"
# python -c "import nltk; nltk.download('omw-1.4')"

# --- Configuration ---
DATA_PATH = os.path.join("data", "pubmed_abstracts_raw.csv")
PROCESSED_DATA_PATH = os.path.join("data", "pubmed_abstracts_processed.csv")
TREND_DATA_PATH = os.path.join("data", "medical_trends.csv") # New output file for trends
TOP_N_KEYWORDS = 500 # How many top keywords/n-grams to track overall
MIN_YEAR = 2015 # Based on your collection start year, filter out stray older ones

# --- Load Data ---
def load_data(filepath):
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    print(f"Initial shape: {df.shape}")
    return df

# --- Initial Cleaning and Preprocessing ---
def preprocess_data(df):
    print("Starting data preprocessing...")
    
    # Drop rows where PMID is missing (shouldn't happen, but good practice)
    df.dropna(subset=['PMID'], inplace=True)
    df.drop_duplicates(subset=['PMID'], inplace=True) # Ensure no duplicates remain
    
    # Convert PublicationYear to integer, drop rows where it's missing or invalid
    df['PublicationYear'] = pd.to_numeric(df['PublicationYear'], errors='coerce')
    df.dropna(subset=['PublicationYear'], inplace=True)
    df['PublicationYear'] = df['PublicationYear'].astype(int)
    
    # Filter out any years before your intended start (e.g., 2014 ones you saw)
    df = df[df['PublicationYear'] >= MIN_YEAR].copy()

    # Combine Title and Abstract for comprehensive text analysis
    # Fill NaN abstracts with empty string to avoid errors in text processing
    # CORRECTED: Avoid inplace=True to silence FutureWarning
    df['Abstract'] = df['Abstract'].fillna('')
    df['Title'] = df['Title'].fillna('')
    df['FullText'] = df['Title'] + " " + df['Abstract']
    
    print(f"Shape after initial cleaning and year filtering ({MIN_YEAR}+): {df.shape}")
    return df

# --- NLP Text Preprocessing ---
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    if not isinstance(text, str):
        return "" # Handle non-string types
    
    # Remove special characters, numbers, and punctuation
    # CORRECTED: Pass flags as keyword argument to silence DeprecationWarning
    text = re.sub(r'[^a-zA-Z\s]', '', text, flags=re.I|re.A)
    # Convert to lowercase
    text = text.lower()
    # Tokenize
    tokens = text.split()
    # Remove stopwords and lemmatize
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and len(word) > 2] # Remove short words
    return " ".join(tokens)

# --- Extract Top TF-IDF Keywords/N-grams ---
def extract_top_tfidf_ngrams(df, text_column='CleanText', n_features=TOP_N_KEYWORDS, ngram_range=(1, 2)):
    """
    Extracts top N TF-IDF unigrams and bigrams from the entire corpus.
    ngram_range=(1,1) for unigrams, (1,2) for unigrams+bigrams, (2,2) for bigrams only.
    """
    print(f"\nExtracting top {n_features} TF-IDF n-grams (range: {ngram_range})...")
    
    # Initialize TF-IDF Vectorizer
    # min_df=5: Ignores terms that appear in less than 5 documents (removes very rare words)
    # max_df=0.8: Ignores terms that appear in more than 80% of documents (removes overly common words)
    vectorizer = TfidfVectorizer(ngram_range=ngram_range, min_df=5, max_df=0.8)
    
    # Fit and transform the clean text data
    tfidf_matrix = vectorizer.fit_transform(df[text_column])
    
    # Get feature names (the words/n-grams)
    feature_names = vectorizer.get_feature_names_out()
    
    # Sum TF-IDF scores for each feature across all documents to get overall importance
    tfidf_scores = tfidf_matrix.sum(axis=0).A1
    
    # Create a Series of scores with feature names as index and sort
    sorted_tfidf_scores = pd.Series(tfidf_scores, index=feature_names).sort_values(ascending=False)
    
    top_ngrams = sorted_tfidf_scores.head(n_features).index.tolist()
    
    print(f"Top {len(top_ngrams)} TF-IDF n-grams identified.")
    return top_ngrams, vectorizer # Return vectorizer for potential re-use or inspection

# --- Calculate Annual Frequencies of Top N-grams ---
def calculate_annual_ngram_frequencies(df, top_ngrams, text_column='CleanText'):
    """
    Calculates the frequency of each top n-gram per year.
    Uses a CountVectorizer to get raw counts (term frequencies)
    for trends, using the pre-selected top_ngrams as its vocabulary.
    """
    print("\nCalculating annual frequencies of top n-grams...")
    annual_trends = []
    
    # Get all unique years
    years = sorted(df['PublicationYear'].unique())
    
    # Initialize a CountVectorizer for getting term frequencies.
    # Pass the *list* of top_ngrams directly as the vocabulary.
    # This creates its own internal, contiguous indices for these terms.
    # Use the same ngram_range as was used for selecting top_ngrams (1,2)
    # CORRECTED: Switched to CountVectorizer
    count_vectorizer = CountVectorizer(ngram_range=(1,2),
                                       vocabulary=top_ngrams # Pass list directly
                                       )
    
    # NO NEED for count_vectorizer.fit([]) here with CountVectorizer and fixed vocabulary

    # Loop through each year to get counts
    for year in tqdm(years, desc="Processing Years"):
        year_df = df[df['PublicationYear'] == year]
        if year_df.empty:
            # If a year has no data, append a row with 0s for that year
            year_data = {'Year': year}
            for ngram in top_ngrams:
                year_data[ngram] = 0
            annual_trends.append(year_data)
            continue # Skip to next year

        # Transform the current year's text using the count_vectorizer
        # This will produce a sparse matrix where columns correspond to top_ngrams
        yearly_count_matrix = count_vectorizer.transform(year_df[text_column])
        
        # Sum the counts for each term for this year across all documents in that year
        yearly_sums = yearly_count_matrix.sum(axis=0).A1
        
        # Create a dictionary for this year's frequencies
        year_data = {'Year': year}
        # Iterate through the feature names of the count_vectorizer (which are our top_ngrams
        # in their new, contiguous index order) and assign their corresponding sum
        for i, ngram in enumerate(count_vectorizer.get_feature_names_out()):
            year_data[ngram] = yearly_sums[i]
        
        annual_trends.append(year_data)
            
    # Create DataFrame from annual trends
    # Ensure all top_ngrams are columns, even if some have 0 counts for certain years
    trends_df = pd.DataFrame(annual_trends).set_index('Year').fillna(0)
    trends_df = trends_df.astype(int) # Ensure counts are integers

    print("Annual frequencies calculated.")
    return trends_df


# --- Main Execution ---
if __name__ == "__main__":
    # 1. Load the raw data
    raw_df = load_data(DATA_PATH)
    
    # 2. Preprocess the data (handle missing values, create FullText column)
    processed_df = preprocess_data(raw_df)
    
    # 3. Apply NLP text cleaning
    print("Applying NLP text cleaning to FullText column (this might take a while)...")
    tqdm.pandas() # Initialize tqdm for pandas apply
    processed_df['CleanText'] = processed_df['FullText'].progress_apply(clean_text)
    
    # Drop rows where CleanText became empty after processing (e.g., if only stopwords)
    processed_df.dropna(subset=['CleanText'], inplace=True)
    processed_df = processed_df[processed_df['CleanText'].str.strip() != ''].copy()

    print(f"Shape after NLP cleaning: {processed_df.shape}")

    # --- Save Processed Data ---
    # Save a CSV with cleaned text for easier debugging and next steps
    processed_df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Processed data saved to: {PROCESSED_DATA_PATH}")

    # --- Trend Spotting ---
    # 4. Extract Top N TF-IDF N-grams (unigrams and bigrams)
    # We pass the vectorizer object from this step for potential reuse, though not strictly needed by the next function's current form.
    top_ngrams, vectorizer = extract_top_tfidf_ngrams(processed_df, ngram_range=(1, 2), n_features=TOP_N_KEYWORDS)
    
    # 5. Calculate Annual Frequencies of these Top N-grams
    # CORRECTED: Removed the 'vectorizer' argument as it's not needed by the corrected function
    trends_df = calculate_annual_ngram_frequencies(processed_df, top_ngrams)
    
    # 6. Save the trend data
    trends_df.to_csv(TREND_DATA_PATH)
    print(f"Annual medical trends saved to: {TREND_DATA_PATH}")

    print("\n--- Phase 2, Step 2.3: Keyword/N-gram Extraction & Frequency Analysis complete! ---")
    print("Next: Visualization and Interpretation of Trends.")

    print("\nFirst 10 rows of the trends data:")
    print(trends_df.head(10))
    print("\nTrends data info:")
    trends_df.info()