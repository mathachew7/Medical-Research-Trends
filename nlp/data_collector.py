import requests
import time
import pandas as pd
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv


load_dotenv() 

# --- Configuration ---
EMAIL = os.getenv("EMAIL") # !!! IMPORTANT: Replace with your actual email !!!
API_KEY = os.getenv("API_KEY") # !!! IMPORTANT: PASTE NCBI API KEY HERE !!!
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
BATCH_SIZE = 500 # Number of PMIDs to fetch per EFetch request
MAX_ABSTRACTS_PER_QUERY = 10000 # Limit for each search query to prevent overwhelming the system
DELAY_BETWEEN_REQUESTS = 0.1 # *** Increased speed: now 10 requests per second with API key ***
OUTPUT_DIR = "data"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_pubmed_ids(query, mindate, maxdate, retmax=10000, email=EMAIL, api_key=API_KEY):
    """
    Searches PubMed for articles and returns PMIDs stored on history server.
    """
    esearch_url = f"{BASE_URL}esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax,
        "mindate": mindate,
        "maxdate": maxdate,
        "usehistory": "y",
        "email": email,
        "api_key": api_key, # <--- API KEY ADDED HERE
    }
    
    print(f"Searching PubMed for '{query}' from {mindate} to {maxdate}...")
    try:
        response = requests.get(esearch_url, params=params)
        response.raise_for_status() 
        data = response.json()
        
        count = int(data["esearchresult"]["count"])
        webenv = data["esearchresult"]["webenv"]
        query_key = data["esearchresult"]["querykey"]

        print(f"Found {count} articles for '{query}'. Storing results on history server.")
        return webenv, query_key, count
    except requests.exceptions.RequestException as e:
        print(f"Error during ESearch: {e}")
        return None, None, 0

def fetch_abstracts_from_history(webenv, query_key, retstart, retmax, email=EMAIL, api_key=API_KEY):
    """
    Fetches article details (including abstract) for a batch of PMIDs
    from the Entrez history server using retstart and retmax.
    """
    efetch_url = f"{BASE_URL}efetch.fcgi"
    
    params = {
        "db": "pubmed",
        "query_key": query_key,
        "webenv": webenv,
        "retmode": "xml",
        "rettype": "abstract",
        "retstart": retstart,
        "retmax": retmax,
        "email": email,
        "api_key": api_key, # <--- API KEY ADDED HERE
    }

    try:
        response = requests.get(efetch_url, params=params)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error during EFetch at retstart={retstart}: {e}")
        return None

def parse_pubmed_xml(xml_content):
    """
    Parses the XML content from EFetch and extracts relevant data.
    """
    articles_data = []
    if not xml_content:
        return articles_data

    try:
        root = ET.fromstring(xml_content)
        
        for article in root.findall(".//PubmedArticle"):
            pmid = article.find(".//PMID")
            title = article.findtext(".//ArticleTitle")
            
            abstract_parts = []
            for abs_text_elem in article.findall(".//AbstractText"):
                if abs_text_elem.text:
                    abstract_parts.append(abs_text_elem.text.strip())
            abstract_full = "\n".join(abstract_parts) if abstract_parts else None

            pub_date_year = article.findtext(".//PubDate/Year")
            pub_date_month = article.findtext(".//PubDate/Month")
            journal_title = article.findtext(".//Journal/Title")

            data = {
                "PMID": pmid.text if pmid is not None else None,
                "Title": title,
                "Abstract": abstract_full,
                "PublicationYear": pub_date_year,
                "PublicationMonth": pub_date_month,
                "JournalTitle": journal_title,
            }
            articles_data.append(data)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}. Content that caused error (first 500 chars):\n{xml_content[:500]}...")
    return articles_data

def collect_data(keywords, start_year, end_year):
    all_articles = []
    
    for year in range(start_year, end_year + 1):
        print(f"\n--- Collecting data for year: {year} ---")
        for keyword in keywords:
            search_term = f"({keyword}) AND ({year}[pdat])"
            
            webenv, query_key, total_count_for_query = fetch_pubmed_ids(
                search_term, f"{year}/01/01", f"{year}/12/31",
                retmax=MAX_ABSTRACTS_PER_QUERY
            )
            
            if total_count_for_query == 0 or webenv is None or query_key is None:
                print(f"No articles found for '{search_term}' or ESearch failed. Skipping to next.")
                time.sleep(DELAY_BETWEEN_REQUESTS)
                continue
            
            num_to_fetch = min(total_count_for_query, MAX_ABSTRACTS_PER_QUERY)
            
            print(f"  -> Attempting to fetch {num_to_fetch} abstracts for '{search_term}' from history...")

            retrieved_articles_count = 0
            
            for retstart_idx in range(0, num_to_fetch, BATCH_SIZE):
                current_batch_size = min(BATCH_SIZE, num_to_fetch - retstart_idx)
                
                xml_data = fetch_abstracts_from_history(
                    webenv, query_key, retstart_idx, current_batch_size
                )
                
                if xml_data:
                    parsed_data = parse_pubmed_xml(xml_data)
                    all_articles.extend(parsed_data)
                    retrieved_articles_count += len(parsed_data)
                    print(f"  -> Processed batch (start={retstart_idx}). Total articles retrieved for '{search_term}': {retrieved_articles_count}/{num_to_fetch}")
                else:
                    print(f"  -> Failed to retrieve XML for batch starting at {retstart_idx}. Stopping for this query.")
                    break
                
                time.sleep(DELAY_BETWEEN_REQUESTS)

            print(f"Finished collecting for '{search_term}'. Total retrieved: {retrieved_articles_count}")

    if all_articles:
        df = pd.DataFrame(all_articles)
        df.drop_duplicates(subset=['PMID'], inplace=True)
        
        df['PublicationYear'] = pd.to_numeric(df['PublicationYear'], errors='coerce')
        df.sort_values(by=['PublicationYear', 'PMID'], inplace=True)
        
        output_filepath = os.path.join(OUTPUT_DIR, "pubmed_abstracts_raw.csv")
        df.to_csv(output_filepath, index=False)
        print(f"\n--- Data collection complete ---")
        print(f"Total unique articles collected: {len(df)}")
        print(f"Raw data saved to: {output_filepath}")
        return df
    else:
        print("\nNo articles were collected.")
        return pd.DataFrame()


if __name__ == "__main__":
    search_keywords = [
        "CRISPR",
        "precision medicine",
        "immunotherapy cancer",
        "digital health",
        "microbiome"
    ]
    
    start_year = 2015
    end_year = 2024

    collected_df = collect_data(search_keywords, start_year, end_year)

    if not collected_df.empty:
        print("\nFirst 5 rows of collected data:")
        print(collected_df.head())
        print("\nData Info:")
        collected_df.info()
    else:
        print("No DataFrame was created.")