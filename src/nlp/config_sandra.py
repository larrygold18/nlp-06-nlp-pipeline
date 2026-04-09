"""
src/nlp/config_sandra.py - Module 6 Configuration
(COPY AND MODIFY THIS FILE - do not edit the original)

Stores configuration values for Sandra's custom web document EVTAL pipeline.
Source: arXiv abstract page for "Agents of Chaos" (2602.20021)

Purpose

  Store configuration values.

Analytical Questions

- What web page URL should be used as the data source?
- Where should raw and processed data be stored?
- How should custom output files be named?

Notes

Following our process, do NOT edit this _case file directly,
keep it as a working example.

In your custom project, copy this _case.py file and
append with _yourname.py instead.

Then edit your copied Python file to change:
- PAGE_URL (source of the HTML web page document),
- customize your output file names.
"""

from pathlib import Path

# ============================================================
# WEB CONFIGURATION
# ============================================================

# Use the same arXiv page for this custom project,
# but customize the downstream logic and output.
PAGE_URL: str = "https://arxiv.org/abs/2602.20021"

# Let the site know who we are and that this is educational use.
HTTP_REQUEST_HEADERS: dict = {
    "User-Agent": "Mozilla/5.0 (Sandra-Otubushin educational web-mining project)"
}

# ============================================================
# PATH CONFIGURATION
# ============================================================

ROOT_PATH: Path = Path.cwd()
DATA_PATH: Path = ROOT_PATH / "data"
RAW_PATH: Path = DATA_PATH / "raw"
PROCESSED_PATH: Path = DATA_PATH / "processed"

# Custom output file names for Sandra's project.
RAW_HTML_PATH: Path = RAW_PATH / "sandra_raw.html"
PROCESSED_CSV_PATH: Path = PROCESSED_PATH / "sandra_processed.csv"
