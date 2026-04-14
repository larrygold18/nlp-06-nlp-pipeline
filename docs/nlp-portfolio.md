# NLP Portfolio: Web Mining and Applied NLP
**Author:** Sandra Otubushin
**Course:** Web Mining and Applied NLP
**Date:** 04/2026

---

## Overview
This portfolio showcases my work applying natural language processing (NLP) techniques to real-world text data from web pages and APIs. My projects focus on building structured, repeatable pipelines to extract, clean, analyze, and interpret text data using Python.

A key focus of my work is transforming messy, unstructured text into meaningful datasets and engineering features that support deeper analysis and visualization.

---

## Key Project Links
- [Project 6: NLP Pipeline (Final Project)](https://github.com/larrygold18/nlp-06-nlp-pipeline)
- [Project 5: Web Document Pipeline](https://github.com/larrygold18/nlp-05-web-documents)
- [Project 4: API JSON Pipeline](https://github.com/larrygold18/nlp-04-api-text-data)

---

## 1. NLP Techniques Implemented

I applied several core NLP techniques across my projects:

- **Tokenization**
  - Split cleaned text into individual tokens using spaCy.
  - Evidence:
    - `tokens` column in processed dataset
    - Transform stage: `stage03_transform_sandra.py`

- **Frequency Analysis**
  - Used `collections.Counter` to compute token frequency.
  - Evidence:
    - Top token chart: `sandra_top_tokens.png`
    - Token frequency table: `sandra_top_tokens_table.csv`

- **Text Cleaning and Normalization**
  - Applied:
    - lowercasing
    - punctuation removal
    - whitespace normalization
    - stopword removal (spaCy)
  - Evidence:
    - Cleaning logic in `_clean_text()` function

- **Feature Engineering**
  - Created derived features including:
    - `token_count`
    - `unique_token_count`
    - `type_token_ratio`
    - `avg_token_length`
    - `lexical_density`
    - `author_count`
  - Evidence:
    - `stage03_transform_sandra.py`

- **Web Scraping (HTML)**
  - Extracted data using BeautifulSoup.
  - Evidence:
    - `pipeline_web_html_sandra.py`

- **Visualization**
  - Created:
    - bar chart (top tokens)
    - word cloud
    - token length histogram
  - Evidence:
    - files in `data/processed/`

---

## 2. Systems and Data Sources

I worked with multiple types of data:

- **Web Pages (HTML)**
  - Source: arXiv research paper page
  - Example: https://arxiv.org/abs/2602.20021

- **APIs (JSON)**
  - NewsAPI (structured JSON data)

- **Data Challenges**
  - HTML contained noise such as labels (`Title:` and `Abstract:`)
  - Required cleaning to remove punctuation and normalize spacing
  - Missing or inconsistent fields required validation checks
  - Structured extraction required identifying correct HTML tags

---

## 3. Pipeline Structure (EVTAL)

My projects followed a structured EVTAL pipeline:

### Extract
- Retrieved HTML using `requests`
- Saved raw file:
  - `data/raw/sandra_raw.html`

### Validate
- Verified required elements:
  - title
  - authors
  - abstract
  - subjects
  - dateline

### Transform
- Extracted structured fields
- Cleaned text
- Created derived NLP features

### Analyze
- Generated:
  - top token bar chart
  - word cloud
  - token length histogram
  - token frequency table

### Load
- Saved processed dataset:
  - `data/processed/sandra_processed.csv`

---

## 4. Signals and Analysis Methods

I computed several important signals:

- **Word Frequency**
  - Identified most common tokens

- **Vocabulary Richness**
  - Type-token ratio

- **Lexical Density**
  - Measures information richness of text

- **Token Structure**
  - Token length distribution

- **Keyword Identification**
  - Frequent tokens representing the topic

---

## 5. Insights

My analysis revealed several insights:

- The abstract shows **moderate to high vocabulary diversity**
- Frequent tokens reflect the paper’s focus on AI systems and agents
- Word cloud highlights dominant themes visually
- Token length distribution shows typical academic writing structure
- Cleaning significantly improved data quality and analysis accuracy

---

## 6. Representative Work

### Project 4: API-Based NLP Pipeline
**Link:** https://github.com/larrygold18/nlp-04-api-text-data

This project demonstrates extracting and processing JSON data from an API and converting it into a structured dataset with derived metrics.

---

### Project 5: Web Document Pipeline
**Link:** https://github.com/larrygold18/nlp-05-web-documents

This project demonstrates extracting and validating HTML data and transforming it into structured tabular format.

---

### Project 6: Full NLP Pipeline (Final Project)
**Link:** https://github.com/larrygold18/nlp-06-nlp-pipeline

This project demonstrates a complete EVTAL pipeline with text cleaning, feature engineering, and visualization, producing multiple analytical outputs.

---

## 7. Skills

Through these projects, I developed:

- Python data processing
- Web scraping with BeautifulSoup
- Working with JSON APIs
- Cleaning and normalizing text data
- Tokenization and NLP feature engineering
- Frequency analysis and visualization
- Handling messy real-world data
- Building reusable EVTAL pipelines
- Debugging and troubleshooting pipelines
- Communicating results using Markdown and visuals

---

## Final Notes

This portfolio reflects my ability to build structured NLP pipelines and extract meaningful insights from real-world text data. I have developed strong skills in data cleaning, transformation, and analysis, and I am confident in applying these techniques to future NLP and data science projects.
