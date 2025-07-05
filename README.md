# MedResearchTrendSpotter | Medical Research Trends Analysis
An NLP-powered pipeline that extracts, analyzes, and visualizes evolving medical research trends using PubMed abstracts (2015–2024).

## 📌 Project Summary
MedResearchTrendSpotter is a robust and complete system designed to identify and analyze high-impact trends within the vast landscape of medical research. By leveraging the PubMed API (via NCBI Entrez) and advanced Natural Language Processing (NLP) techniques, it collects and processes medical abstracts, extracts significant keywords and n-grams, and generates comprehensive trend data. The extracted insights are then presented through an interactive web-based dashboard, offering visual insights into emerging research themes.

This tool is built to empower researchers, academic institutions, and policymakers by providing an automated and efficient way to discover and monitor the evolution of medical research trends, facilitating informed decision-making and strategic planning.

## 🚀 Features
-Automated Abstract Collection: Seamlessly gathers medical abstracts and metadata from PubMed using the NCBI Entrez API for a specified keyword and year range.

-Comprehensive Text Processing: Implements a robust NLP pipeline including:

 - Text Cleaning (lowercase, punctuation/number removal).

 - Stopword Removal.

 - Lemmatization.

 - TF-IDF (Term Frequency-Inverse Document Frequency) for keyword importance.

- Unigram & Bigram Extraction: Identifies and ranks significant single words (unigrams) and two-word phrases (bigrams) based on their frequency and TF-IDF scores.

- Annual Trend Calculation: Computes the yearly frequency of each extracted term, generating a valuable trend matrix.

- Data Export: Produces clean CSV files for raw, processed, and trend-specific data, along with JSON for category mappings.

- Interactive Web Dashboard: A user-friendly frontend built with HTML and powered by Chart.js for dynamic and insightful visualizations, including:

  - Line charts for "Trends Over Time".

  - Donut/Pie charts for "Top Keywords" distribution.

  - Bar charts for "Forecast" predictions.

  - Keyword co-occurrence visualization (conceptually a word cloud).

  - Direct links to "Recent Abstracts".

  - Future-ready for data filtering by category and year range.

## 📁 Folder Structure
```
MedResearchTrendSpotter/
├── data/
│   ├── pubmed_abstracts_raw.csv         # Raw downloaded abstracts from PubMed
│   ├── pubmed_abstracts_processed.csv   # Cleaned and NLP-processed text
│   ├── medical_trends.csv               # Term frequency matrix per year (main trend data)
│   ├── term_category_backtrack.json     # Mapping of extracted terms to broader categories
│   └── category_trends.csv              # Aggregated term counts summed by category
├── static/
│   └── script.js                        # JavaScript logic for dashboard charts and interactivity
├── templates/
│   └── index.html                       # Main HTML file for the interactive dashboard
├── .env                                 # Environment variables (e.g., API keys, email)
├── .gitignore                           # Specifies intentionally untracked files to ignore
├── app.py                               # Flask web application backend
├── data_collector.py                    # Script to collect data from PubMed API
├── nlp_processor.py                     # Script for text preprocessing and TF-IDF analysis
├── trend_visualizer.py (optional)       # Placeholder for potential future dedicated visualization script
├── requirements.txt                     # Python dependencies for the project
└── README.md                            # Project documentation (this file)

```
---

## 🧠 How It Works
The MedResearchTrendSpotter operates through a sequential, modular pipeline:


Step 1: Data Collection
 - Script: data_collector.py

 - Functionality: This script establishes a connection to the PubMed database via the NCBI Entrez API. It efficiently downloads relevant metadata and full abstracts based on a specified primary keyword and a defined year range (e.g., 2015-2024).

 - Output: The raw, collected data is saved as data/pubmed_abstracts_raw.csv.

Step 2: Text Preprocessing & Analysis
 - Script: nlp_processor.py

 - Functionality: This core NLP script performs several critical operations:

  - Cleaning: It cleans and merges the abstract and title fields from the raw data.

  - NLP Pipeline: Applies a series of Natural Language Processing steps, including converting text to lowercase, removing punctuation and numbers, eliminating common stopwords, and lemmatizing words to their base forms.

  - Keyword Extraction: Utilizes TF-IDF (Term Frequency-Inverse Document Frequency) to identify the top 500 most significant keywords, including both unigrams (single words) and bigrams (two-word phrases).

  - Trend Tracking: Systematically tracks the yearly frequency of each extracted term, which is crucial for trend analysis.

 - Output: Processed text is saved in data/pubmed_abstracts_processed.csv, and the term frequency matrix is generated as data/medical_trends.csv. Additional mapping and aggregated category data are stored in data/term_category_backtrack.json and data/category_trends.csv.

Step 3: Dashboard & Visualization
 - Frontend: templates/index.html (HTML structure) + static/script.js (JavaScript for interactivity)

- Functionality: This component provides an intuitive and interactive user interface to explore the analyzed trends:

  - Interactive Charts: Displays "Trends Over Time" using line charts, "Top Keywords" distribution via donut/pie charts, and "Forecast" insights through bar charts. These are rendered dynamically using Chart.js.

  - Keyword Co-occurrence: Visualizes relationships between keywords (conceptually as a word cloud or network).

  - Recent Abstracts: Presents a list of recent abstracts with links, allowing users to quickly access source information.

  - Filtering Capabilities: Designed to support future filters by category and year range, enhancing data exploration.

## 📊 Output Files
 - pubmed_abstracts_raw.csv: Contains the original, unprocessed data downloaded directly from PubMed.

 - pubmed_abstracts_processed.csv: Stores the abstracts after text cleaning and NLP preprocessing, including a CleanText column.

 - medical_trends.csv: A matrix detailing the frequency of each extracted term across different years, forming the basis for trend analysis.

 - category_trends.csv: Aggregated counts of terms, summed by their respective broader categories, useful for high-level trend overviews.

 - term_category_backtrack.json: A JSON file providing a mapping from specific extracted terms back to their assigned categories, facilitating filtering and categorization.

## 🖥️ Local Setup & Running Instructions
Follow these steps to get MedResearchTrendSpotter up and running on your local machine.

1. Clone the Repository
Begin by cloning the project repository from GitHub:

```
git clone [https://github.com/mathachew7/MedResearchTrendSpotter.git](https://github.com/mathachew7/MedResearchTrendSpotter.git)
cd MedResearchTrendSpotter
```

2. Create & Activate Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies:

```
python -m venv venv
```
Activate the virtual environment:

 - macOS/Linux:
 ```
  source venv/bin/activate
 ```
 - Windows (Command Prompt):
 ```
  venv\Scripts\activate.bat
 ```
 - Windows (PowerShell):
 ```
  .\venv\Scripts\Activate.ps1
 ```
3. Install Dependencies
Install all required Python packages using pip:
```
pip install -r requirements.txt
```
4. Download NLTK Assets
Some NLP functionalities require specific NLTK data packages. Download them:
```
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
```
5. Setup .env File
Create a file named .env in the root directory of your project. This file will store your sensitive API key and email for accessing the NCBI PubMed API.
```
NCBI_API_KEY=your_ncbi_api_key_here
NCBI_EMAIL=your_email@example.com
```
Important: Replace your_ncbi_api_key_here with your actual NCBI API key obtained from NCBI. Replace your_email@example.com with your valid email address, as it's required by the Entrez API.

6. Run the Scripts
Execute the pipeline scripts in the following order:

Collect PubMed Abstracts
This will fetch raw data from PubMed.
```
python data_collector.py
```
Run NLP Processing + Generate Trend CSV
This will clean the data, apply NLP, and generate trend metrics.
```
python nlp_processor.py
```
Start the Flask Dashboard
This will launch the web server for the interactive dashboard.
```
python app.py
```
Once the Flask app is running, open your web browser and navigate to:


### 🌐 http://localhost:5000

## 🔮 Future Enhancements
 - 🔍 Searchable Abstracts: Implement a search functionality within the dashboard, allowing users to search abstracts with keyword highlighting.

 - 📈 Advanced Visualizations: Integrate category-wise heatmaps and develop algorithms for automated trend acceleration detection.

 - 🧠 Biomedical Tagging: Explore integration with specialized NLP libraries like SciSpacy for more advanced and domain-specific biomedical entity recognition and tagging.

 - 📦 Dockerization: Package the entire application into Docker containers for easier deployment and environment consistency.

 - User Authentication: Add user login and authentication for personalized dashboards or data access control.

 - Database Integration: Replace CSV files with a proper database (e.g., PostgreSQL, MongoDB) for more robust data storage and querying.

## 🤝 Acknowledgments
This project utilizes and builds upon the following incredible resources and libraries:

 - PubMed / NCBI Entrez API

 - NLTK (Natural Language Toolkit)

 - Scikit-learn

 - Flask (Web Framework)

 - Chart.js (JavaScript Charting Library)

 - Tailwind CSS (Utility-first CSS Framework)

## 📬 Contact
Feel free to reach out for questions, feedback, or collaborations!

 - 📧 Email: subashyadav7@outlook.com

 - 🌐 LinkedIn: linkedin.com/in/mathachew7

## 📄 License
This project is licensed under the MIT License. See the LICENSE file (if you have one, or you can create one) for more details.
