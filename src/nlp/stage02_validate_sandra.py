"""
src/nlp/stage02_validate_sandra.py - Validate Stage
(EDIT YOUR COPY OF THIS FILE)

Source: Raw HTML string
Sink:   BeautifulSoup object (in memory)

Purpose

  Validate that the expected page structure is present.

Analytical Questions

- What is the top-level structure of the HTML document?
- What elements are present in the document?
- Does the data meet expectations for transformation?
- Are additional custom fields available for extraction?

Notes

Following our process, do NOT edit this _case file directly,
keep it as a working example.

In your custom project, copy this _case.py file and
append with _yourname.py instead.

Then edit your copied Python file to:
- inspect the HTML structure,
- validate required elements,
- confirm the data is usable for your analysis.
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging

from bs4 import BeautifulSoup

# ============================================================
# Section 2. Define Run Validate Function
# ============================================================


def run_validate(
    html_content: str,
    LOG: logging.Logger,
) -> BeautifulSoup:
    """Inspect and validate HTML structure.

    Args:
        html_content (str): The raw HTML content from the Extract stage.
        LOG (logging.Logger): The logger instance.

    Returns:
        BeautifulSoup: The validated BeautifulSoup object.
    """

    LOG.info("========================")
    LOG.info("STAGE 02: VALIDATE starting...")
    LOG.info("========================")

    # ============================================================
    # INSPECT HTML STRUCTURE
    # ============================================================

    LOG.info("HTML STRUCTURE INSPECTION:")

    # Parse the HTML content using BeautifulSoup.
    soup = BeautifulSoup(html_content, "html.parser")

    # Log the type of the parsed object.
    LOG.info(f"Top-level type: {type(soup).__name__}")

    # Log top-level elements in the HTML document.
    LOG.info(
        f"Top-level elements: {[element.name for element in soup.find_all(recursive=False)]}"
    )

    # ============================================================
    # VALIDATE EXPECTATIONS
    # ============================================================

    # Check for expected structural elements from the arXiv page.
    title = soup.find("h1", class_="title")
    authors = soup.find("div", class_="authors")
    abstract = soup.find("blockquote", class_="abstract")
    subjects = soup.find("div", class_="subheader")
    dateline = soup.find("div", class_="dateline")

    # Additional custom validation checks.
    canonical = soup.find("link", rel="canonical")
    pdf_link = soup.find("a", class_="abs-button download-pdf")

    LOG.info("VALIDATE: Title found: %s", title is not None)
    LOG.info("VALIDATE: Authors found: %s", authors is not None)
    LOG.info("VALIDATE: Abstract found: %s", abstract is not None)
    LOG.info("VALIDATE: Subjects found: %s", subjects is not None)
    LOG.info("VALIDATE: Dateline found: %s", dateline is not None)
    LOG.info("VALIDATE: Canonical link found: %s", canonical is not None)
    LOG.info("VALIDATE: PDF link found: %s", pdf_link is not None)

    # Collect missing required elements.
    missing = []
    if not title:
        missing.append("title")
    if not authors:
        missing.append("authors")
    if not abstract:
        missing.append("abstract")
    if not subjects:
        missing.append("subjects")
    if not dateline:
        missing.append("dateline")
    if not canonical:
        missing.append("canonical")
    if not pdf_link:
        missing.append("pdf_link")

    # If anything required is missing, stop the pipeline with an error.
    if missing:
        raise ValueError(
            f"VALIDATE: Required elements missing: {missing}. "
            "Page structure may have changed."
        )

    LOG.info("VALIDATE: HTML structure is valid.")
    LOG.info("Sink: validated BeautifulSoup object")

    # Return the validated BeautifulSoup object for use in the next stage.
    return soup
