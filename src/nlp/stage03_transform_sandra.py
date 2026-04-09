"""
stage03_transform_sandra.py
(EDIT YOUR COPY OF THIS FILE)

Source: validated BeautifulSoup object
Sink:   analysis-ready Pandas DataFrame

Purpose

  Transform validated HTML into a clean, analysis-ready DataFrame.

Analytical Questions

- What metadata can be extracted from the web page?
- What cleaning steps improve the text for analysis?
- What derived features would support NLP analysis?
- How can a richer custom output improve downstream analysis?

Notes

- This custom version extends the original case version.
- It extracts additional metadata such as the PDF URL.
- It engineers additional features such as:
    - author_count
    - abstract_char_count
    - unique_token_count
    - type_token_ratio
    - avg_token_length
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging
import re
import string

from bs4 import BeautifulSoup, Tag
import pandas as pd
import spacy

# Load the spaCy English model.
# Download once before use:
#   uv run python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

# ============================================================
# Section 2. Define Helper Functions
# ============================================================


def _get_text(element: Tag | None, strip_prefix: str = "", separator: str = "") -> str:
    """Return element text or 'unknown' if element is None.

    Args:
        element (Tag | None): A BeautifulSoup Tag or None.
        strip_prefix (str): Text prefix to remove from the result.
        separator (str): Separator for get_text(); empty string by default.

    Returns:
        str: Extracted and cleaned text, or 'unknown' if element is None.
    """
    if element is None:
        return "unknown"

    text = element.get_text(separator=separator, strip=True)
    return text.replace(strip_prefix, "").strip() if strip_prefix else text


def _clean_text(text: str, nlp_model: spacy.language.Language) -> str:
    """Clean and normalize a text string for NLP analysis.

    Cleaning steps applied in order:
      1. Lowercase
      2. Remove punctuation
      3. Normalize whitespace
      4. Remove stopwords using spaCy

    Args:
        text (str): Raw text string to clean.
        nlp_model: Loaded spaCy language model.

    Returns:
        str: Cleaned text string.
    """
    # Lowercase text so word comparisons are consistent.
    text = text.lower()

    # Remove punctuation to reduce noise for token analysis.
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Normalize whitespace.
    text = re.sub(r"\s+", " ", text).strip()

    # Remove stopwords and spaces using spaCy.
    doc = nlp_model(text)
    text = " ".join(
        [token.text for token in doc if not token.is_stop and not token.is_space]
    )

    return text


# ============================================================
# Section 3. Define Run Transform Function
# ============================================================


def run_transform(
    soup: BeautifulSoup,
    LOG: logging.Logger,
) -> pd.DataFrame:
    """Transform HTML into a clean, analysis-ready DataFrame.

    Args:
        soup (BeautifulSoup): Validated BeautifulSoup object.
        LOG (logging.Logger): The logger instance.

    Returns:
        pd.DataFrame: The transformed and analysis-ready dataset.
    """

    LOG.info("========================")
    LOG.info("STAGE 03: TRANSFORM starting...")
    LOG.info("========================")

    # ============================================================
    # PHASE 3.1: Extract raw fields from HTML
    # ============================================================

    LOG.info("========================")
    LOG.info("PHASE 3.1: Extract raw fields from HTML")
    LOG.info("========================")

    # Extract title.
    title_tag: Tag | None = soup.find("h1", class_="title")
    title: str = _get_text(title_tag, strip_prefix="Title:")

    # Extract authors.
    authors_tag: Tag | None = soup.find("div", class_="authors")
    author_tags_list: list[Tag] = authors_tag.find_all("a") if authors_tag else []
    authors: str = (
        ", ".join([tag.get_text(strip=True) for tag in author_tags_list])
        if authors_tag
        else "unknown"
    )

    # Extract abstract.
    abstract_tag: Tag | None = soup.find("blockquote", class_="abstract")
    abstract_raw: str = _get_text(abstract_tag, strip_prefix="Abstract:")

    # Extract subjects.
    subheader: Tag | None = soup.find("div", class_="subheader")
    subjects: str = _get_text(subheader, strip_prefix="Subjects:")

    # Extract submitted date.
    dateline: Tag | None = soup.find("div", class_="dateline")
    submitted: str = _get_text(dateline)

    # Extract arXiv ID from canonical link.
    canonical: Tag | None = soup.find("link", rel="canonical")
    if canonical is None:
        arxiv_id = "unknown"
    else:
        href = str(canonical["href"])
        arxiv_id = href.split("/abs/")[-1]

    # Extract PDF URL.
    pdf_tag: Tag | None = soup.find("a", class_="abs-button download-pdf")
    if pdf_tag is not None and pdf_tag.has_attr("href"):
        pdf_url = str(pdf_tag["href"])
        if pdf_url.startswith("/"):
            pdf_url = f"https://arxiv.org{pdf_url}"
    else:
        pdf_url = "unknown"

    LOG.info(f"Extracted title: {title}")
    LOG.info(f"Extracted authors: {authors}")
    LOG.info(f"Extracted subjects: {subjects}")
    LOG.info(f"Extracted submitted date: {submitted}")
    LOG.info(f"Extracted arxiv_id: {arxiv_id}")
    LOG.info(f"Extracted pdf_url: {pdf_url}")

    # ============================================================
    # PHASE 3.2: Clean and normalize text fields
    # ============================================================

    LOG.info("========================")
    LOG.info("PHASE 3.2: Clean and normalize text fields")
    LOG.info("========================")

    abstract_clean: str = (
        _clean_text(abstract_raw, nlp) if abstract_raw != "unknown" else "unknown"
    )

    LOG.info(f"abstract raw preview: {abstract_raw[:120]}...")
    LOG.info(f"abstract clean preview: {abstract_clean[:120]}...")

    # ============================================================
    # PHASE 3.3: Engineer derived features
    # ============================================================

    LOG.info("========================")
    LOG.info("PHASE 3.3: Engineer derived features")
    LOG.info("========================")

    # Count words in raw abstract.
    abstract_word_count: int = (
        len(abstract_raw.split()) if abstract_raw != "unknown" else 0
    )

    # Count characters in raw abstract.
    abstract_char_count: int = len(abstract_raw) if abstract_raw != "unknown" else 0

    # Count authors.
    author_count: int = len(author_tags_list)

    # Tokenize cleaned abstract.
    tokens: list[str] = abstract_clean.split() if abstract_clean != "unknown" else []
    token_count: int = len(tokens)

    # Count unique tokens.
    unique_token_count: int = len(set(tokens))

    # Compute type-token ratio.
    type_token_ratio: float = (
        round(unique_token_count / token_count, 4) if token_count > 0 else 0.0
    )

    # Compute average token length.
    avg_token_length: float = (
        round(sum(len(token) for token in tokens) / token_count, 2)
        if token_count > 0
        else 0.0
    )

    LOG.info(f"author_count: {author_count}")
    LOG.info(f"abstract_word_count: {abstract_word_count}")
    LOG.info(f"abstract_char_count: {abstract_char_count}")
    LOG.info(f"token_count: {token_count}")
    LOG.info(f"unique_token_count: {unique_token_count}")
    LOG.info(f"type_token_ratio: {type_token_ratio}")
    LOG.info(f"avg_token_length: {avg_token_length}")

    # ============================================================
    # PHASE 3.4: Build record and create DataFrame
    # ============================================================

    LOG.info("========================")
    LOG.info("PHASE 3.4: Build record and create DataFrame")
    LOG.info("========================")

    record = {
        "arxiv_id": arxiv_id,
        "title": title,
        "authors": authors,
        "author_count": author_count,
        "subjects": subjects,
        "submitted": submitted,
        "pdf_url": pdf_url,
        "abstract_raw": abstract_raw,
        "abstract_clean": abstract_clean,
        "tokens": " ".join(tokens),
        "abstract_word_count": abstract_word_count,
        "abstract_char_count": abstract_char_count,
        "token_count": token_count,
        "unique_token_count": unique_token_count,
        "type_token_ratio": type_token_ratio,
        "avg_token_length": avg_token_length,
    }

    df = pd.DataFrame([record])

    LOG.info(f"Created DataFrame with {len(df)} row and {len(df.columns)} columns")
    LOG.info(f"Columns: {list(df.columns)}")
    LOG.info(
        f"DF preview:\n{df[['arxiv_id', 'title', 'author_count', 'token_count', 'type_token_ratio']].head()}"
    )

    LOG.info("Sink: Pandas DataFrame created")
    LOG.info("Transformation complete.")

    # Return the transformed DataFrame for use in the Analyze and Load stages.
    return df
