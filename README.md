# MedResearchTrendSpotter | Medical-Research-Trends
An NLP-driven tool to identify and visualize trends in medical research from PubMed abstracts.

## Overview
The **MedResearchTrendSpotter** is a Python-based project designed to identify and visualize emerging trends in medical research. It automates the collection of PubMed abstracts, performs natural language processing (NLP) to extract key concepts (unigrams and bigrams), and then analyzes their frequency over time to spotlight trending topics.

This tool visualizes trends in PubMed abstracts (2015–2024) using NLP. Built to help researchers, educators, and policymakers understand what’s changing in medical research.


## Features
- **PubMed Data Collection:** Fetches medical abstract data from PubMed using its API (requires an NCBI API Key).
- **Robust Data Preprocessing:** Cleans and prepares raw abstract text, handling missing values, standardizing formats, and combining relevant text fields.
- **Advanced NLP:** Applies text cleaning (removing special characters, numbers, stopwords), lemmatization, and TF-IDF (Term Frequency-Inverse Document Frequency) to identify the most significant unigrams (single words) and bigrams (two-word phrases).
- **Trend Analysis:** Calculates the annual frequency of the top identified medical concepts to show their evolution over different years.
- **Structured Output:** Saves processed data and trend analysis results into clean CSV files.

## Project Structure
📁 Project Structure

```markdown
MedResearchTrendSpotter/
├── data/
│   ├── pubmed_abstracts_raw.csv         # Raw abstracts collected from PubMed
│   ├── pubmed_abstracts_processed.csv   # Cleaned and NLP-processed abstracts
│   └── medical_trends.csv               # Annual frequencies of top medical keywords/n-grams
├── .env.example                         # Example for environment variables (.env file)
├── .gitignore                           # Specifies files/directories to ignore in Git
├── data_collector.py                    # Script for collecting data from PubMed
├── nlp_processor.py                     # Script for NLP processing and trend analysis
├── requirements.txt                     # List of Python dependencies
└── README.md                            # This documentation file

```

---

## The Journey So Far: Problem, Process, and Progress

### 🎯 What Problem Are We Solving?

Imagine you're a medical researcher, a healthcare policy maker, or someone just deeply interested in how medical science evolves. You want to know:

- ❓ *What diseases are getting more attention this year compared to five years ago?*
- ❓ *Are there new treatment approaches gaining traction?*
- ❓ *Is research shifting towards gene therapy or away from traditional pharmaceuticals?*

Reading hundreds of thousands of scientific papers manually is impossible.  
That’s where **MedResearchTrendSpotter** comes in! We're **turning thousands of medical papers into actionable trend insights.**

### 🔍 What We're Building (The "Why")

Our goal is to build an automated **“trend radar”** for medical research using **Natural Language Processing (NLP)** and programming.

We aim to:

- 📥 **Gather massive datasets** from PubMed (medical abstracts).
- 🧹 **Clean and preprocess** the text for machine understanding.
- 🧠 **Extract keywords & buzzwords** using smart algorithms.
- 📊 **Track term usage over time** to identify trends.
- 📈 **Visualize those trends** to get a bird’s-eye view of the evolution of medical research.

### ✅ What We've Accomplished

#### Phase 1: 🕵️ The Data Hunter (Data Collection)

**Script:** `data_collector.py`

- Connects to the **PubMed API** using an API key and email.
- Collects abstracts from a defined date range (e.g., 2015–present).
- Saves results into: `data/pubmed_abstracts_raw.csv`

> 🔹 *“You can't analyze what you don't have!”*

#### Phase 2: ⚗️ The Data Alchemist (Processing & Trend Analysis)

**Script:** `nlp_processor.py`

This script transforms raw text into meaningful insights.

##### Step 2.1: Initial Data Cleanup

- Filters papers by year.
- Handles missing abstracts/titles.
- Combines title + abstract into a single `FullText` column.

##### Step 2.2: Deep NLP Cleaning

For each abstract:
- Removes punctuation, numbers, and special characters.
- Converts text to lowercase.
- Tokenizes text into words.
- Removes stopwords (e.g., "the", "is").
- Lemmatizes words (e.g., "running", "ran" → "run").

→ Results in a new `CleanText` column.

##### Step 2.3: Key Concepts Extraction (TF-IDF)

- Applies **TF-IDF (Term Frequency-Inverse Document Frequency)** on clean text.
- Extracts top **500 keywords/n-grams** (e.g., "gene therapy", "cell culture").

##### Step 2.4: Tracking Annual Frequencies

- For each year, counts how often each top keyword appears.
- Builds a year-by-year frequency matrix.

📂 **Outputs:**
- `data/pubmed_abstracts_processed.csv` – With clean text per paper.
- `data/medical_trends.csv` – Rows = years, Columns = buzzwords, Values = frequencies.

---

## 📈 What's Next: The Storyteller (Data Visualization)

### Phase 3: 📊 Visualizing the Trends

**Script:** `trend_visualizer.py` (Coming Up)

#### What it will do:

- Load `data/medical_trends.csv`
- Use **Matplotlib**, **Seaborn**, or **Plotly** for visualization.

#### Types of Charts:

- 📉 **Line Charts:** Show term frequency trends over time.
- 📊 **Bar Charts:** Show most popular terms per year.
- 🌡️ **Heatmaps:** Show term shifts across years.
- 🚀 **Emerging Trends:** Spot sudden rises of new keywords.

#### Why it matters:

A CSV file can’t tell a story — a beautiful chart can!

- Instantly see **rising research topics**
- Spot **declining interest areas**
- Identify **breakthroughs and innovations**

📦 **Final Output:** A collection of graphs that reveal **what’s hot and what’s not** in the world of medical research.

---

## Setup and Installation

### Prerequisites
- Python 3.8+
- Git

### Steps

1.  **Clone the Repository:**
    First, clone this repository to your local machine:
    ```bash
    git clone [https://github.com/mathachew7/MedResearchTrendSpotter.git](https://github.com/mathachew7/MedResearchTrendSpotter.git)
    cd MedResearchTrendSpotter
    ```

2.  **Create a Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    -   **Windows (Command Prompt):**
        ```bash
        venv\Scripts\activate.bat
        ```
    -   **Windows (PowerShell):**
        ```bash
        venv\Scripts\Activate.ps1
        ```

4.  **Install Dependencies:**
    Install all required Python packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

5.  **NLTK Data Download:**
    The project uses NLTK for stopwords and lemmatization. You need to download these datasets once:
    ```bash
    python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
    ```

6.  **Set up Environment Variables:**
    Create a `.env` file in the root directory of the project based on `.env.example`. This file will store your sensitive API key and email.
    ```
    # .env
    NCBI_API_KEY=YOUR_NCBI_API_KEY
    NCBI_EMAIL=YOUR_EMAIL@example.com
    ```
    **Replace `YOUR_NCBI_API_KEY` with your actual NCBI API key** (you can obtain one from the [NCBI Developer's page](https://www.ncbi.nlm.nih.gov/account/settings/)).
    **Replace `YOUR_EMAIL@example.com` with your actual email address.** NCBI requires this for API usage.

## Usage

After setting up, run the scripts in the following order:

1.  **Collect Data:**
    This script fetches abstracts from PubMed and saves them to `data/pubmed_abstracts_raw.csv`.
    ```bash
    python data_collector.py
    ```

2.  **Process Data and Analyze Trends:**
    This script cleans the raw data, applies NLP, extracts top keywords/n-grams, and calculates their annual frequencies, saving the results to `data/medical_trends.csv`.
    ```bash
    python nlp_processor.py
    ```

## Output Files
-   `data/pubmed_abstracts_raw.csv`: The initial dataset collected from PubMed.
-   `data/pubmed_abstracts_processed.csv`: The dataset after initial cleaning and NLP text cleaning (`CleanText` column added).
-   `data/medical_trends.csv`: A CSV file containing the yearly counts of the top medical keywords and n-grams, ready for visualization.

## Acknowledgements
We extend our sincere gratitude to the **National Center for Biotechnology Information (NCBI)** for providing access to the PubMed database and its robust API. This project relies heavily on the availability of their comprehensive data for medical research abstracts.

## Contributing
Contributions are welcome! If you have suggestions for improvements, please open an issue or submit a pull request.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 💬 Contact

For collab or publication inquiries:  
📧 subashyadav7@outlook.com  
🔗 [LinkedIn](https://www.linkedin.com/in/mathachew7)
