"""
src/nlp/pipeline_web_html_sandra.py - Module 6 Custom Script

Purpose

  Orchestrate Sandra's custom EVTAL pipeline for web document data.
  Illustrate how to fetch an HTML page, validate its structure,
  transform and clean it into structured data,
  analyze patterns in the text, and load results into a sink.

Analytical Questions

- How can we fetch an HTML page from the web and save it to a file?
- How can we validate the structure and content of an HTML document?
- How can we transform HTML into clean, analysis-ready structured data?
- How can we analyze text data to surface frequency patterns and visualizations?
- How can we load the transformed data into a sink (like a CSV file)?

Notes

- This is Sandra's custom copy of the pipeline.
- It uses Sandra's custom configuration and stage files.
- The original case files remain unchanged.

Run from root project folder with:

  uv run python -m nlp.pipeline_web_html_sandra
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging

from datafun_toolkit.logger import get_logger, log_header, log_path

from nlp.config_sandra import (
    DATA_PATH,
    HTTP_REQUEST_HEADERS,
    PAGE_URL,
    PROCESSED_CSV_PATH,
    PROCESSED_PATH,
    RAW_HTML_PATH,
    RAW_PATH,
    ROOT_PATH,
)
from nlp.stage01_extract import run_extract
from nlp.stage02_validate_sandra import run_validate
from nlp.stage03_transform_sandra import run_transform
from nlp.stage04_analyze_sandra import run_analyze
from nlp.stage05_load import run_load

# ============================================================
# Section 2. Configure Logging
# ============================================================

LOG: logging.Logger = get_logger("CI", level="DEBUG")

# ============================================================
# Section 3. Define Main Pipeline Function
# ============================================================


def main() -> None:
    """Run Sandra's custom EVTAL pipeline."""

    log_header(LOG, "Module 6: Sandra Custom EVTAL PIPELINE - WEB DOCUMENTS (HTML)")
    LOG.info("START PIPELINE")

    # Ensure required folders exist before writing outputs.
    RAW_PATH.mkdir(parents=True, exist_ok=True)
    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

    # Log project paths.
    log_path(LOG, "ROOT_PATH", ROOT_PATH)
    log_path(LOG, "DATA_PATH", DATA_PATH)
    log_path(LOG, "RAW_PATH", RAW_PATH)
    log_path(LOG, "PROCESSED_PATH", PROCESSED_PATH)

    # ============================================================
    # EXTRACT
    # ============================================================

    html_content = run_extract(
        source_url=PAGE_URL,
        http_request_headers=HTTP_REQUEST_HEADERS,
        raw_html_path=RAW_HTML_PATH,
        LOG=LOG,
    )

    # ============================================================
    # VALIDATE
    # ============================================================

    validated_soup = run_validate(
        html_content=html_content,
        LOG=LOG,
    )

    # ============================================================
    # TRANSFORM
    # ============================================================

    df = run_transform(
        soup=validated_soup,
        LOG=LOG,
    )

    # ============================================================
    # ANALYZE
    # ============================================================

    run_analyze(
        df=df,
        LOG=LOG,
    )

    # ============================================================
    # LOAD
    # ============================================================

    run_load(
        df=df,
        processed_csv_path=PROCESSED_CSV_PATH,
        LOG=LOG,
    )

    LOG.info("========================")
    LOG.info("Pipeline executed successfully!")
    LOG.info("========================")


# ============================================================
# Section 4. Run Main Function when This File is Executed
# ============================================================

if __name__ == "__main__":
    main()
