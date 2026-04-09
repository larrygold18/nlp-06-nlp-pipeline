"""
stage04_analyze_sandra.py
(EDIT YOUR COPY OF THIS FILE)

Source: analysis-ready Pandas DataFrame
Sink:   visualizations saved to data/processed/

Purpose

  Compute frequency distributions and produce visualizations
  that surface patterns in the cleaned text.

Analytical Questions

- Which words appear most frequently in the cleaned abstract?
- Does the frequency distribution look meaningful or noisy?
- What does the word cloud reveal about the paper topic?
- What does token length distribution show about the text?
- What does the type-token ratio tell us about vocabulary richness?

Notes

- This custom version extends the original case version.
- It adds a third visualization:
    - token length histogram
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

from collections import Counter
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

# ============================================================
# Section 2. Define Helper Functions
# ============================================================


def _plot_top_tokens(
    tokens: list[str],
    top_n: int,
    output_path: Path,
    title: str,
    LOG: logging.Logger,
) -> None:
    """Plot a horizontal bar chart of the top N most frequent tokens."""
    counter = Counter(tokens)
    most_common = counter.most_common(top_n)

    if not most_common:
        LOG.warning("No tokens to plot.")
        return

    words, counts = zip(*most_common, strict=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(list(reversed(words)), list(reversed(counts)))
    ax.set_xlabel("Frequency")
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    LOG.info(f"Saved bar chart to {output_path}")


def _plot_wordcloud(
    text: str,
    output_path: Path,
    title: str,
    LOG: logging.Logger,
) -> None:
    """Generate and save a word cloud from cleaned text."""
    if not text or text == "unknown":
        LOG.warning("No text available for word cloud.")
        return

    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        max_words=80,
    ).generate(text)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    LOG.info(f"Saved word cloud to {output_path}")


def _plot_token_length_histogram(
    tokens: list[str],
    output_path: Path,
    title: str,
    LOG: logging.Logger,
) -> None:
    """Plot a histogram of token lengths."""
    if not tokens:
        LOG.warning("No tokens available for histogram.")
        return

    token_lengths = [len(token) for token in tokens]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(token_lengths, bins=10)
    ax.set_xlabel("Token Length")
    ax.set_ylabel("Frequency")
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    LOG.info(f"Saved token length histogram to {output_path}")


# ============================================================
# Section 3. Define Run Analyze Function
# ============================================================


def run_analyze(
    df: pd.DataFrame,
    LOG: logging.Logger,
    output_dir: Path = Path("data/processed"),
    top_n: int = 15,
) -> None:
    """Analyze the transformed DataFrame and produce visualizations.

    Args:
        df (pd.DataFrame): Analysis-ready DataFrame from Transform stage.
        LOG (logging.Logger): The logger instance.
        output_dir (Path): Directory to save visualization outputs.
        top_n (int): Number of top tokens to show in frequency chart.
    """

    LOG.info("========================")
    LOG.info("STAGE 04: ANALYZE starting...")
    LOG.info("========================")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Extract values from the first row.
    row = df.iloc[0]

    title: str = str(row.get("title", "unknown"))
    tokens_str: str = str(row.get("tokens", ""))
    type_token_ratio: float = float(row.get("type_token_ratio", 0.0))
    author_count: int = int(row.get("author_count", 0))
    avg_token_length: float = float(row.get("avg_token_length", 0.0))

    # Convert the saved token string back to a list.
    tokens: list[str] = tokens_str.split() if tokens_str else []

    LOG.info(f"Paper: {title}")
    LOG.info(f"Type-token ratio: {type_token_ratio}")
    LOG.info(f"Author count: {author_count}")
    LOG.info(f"Average token length: {avg_token_length}")

    # ============================================================
    # PHASE 4.1: Top token frequency bar chart
    # ============================================================

    LOG.info("========================")
    LOG.info(f"PHASE 4.1: Top {top_n} token frequency - bar chart")
    LOG.info("========================")

    _plot_top_tokens(
        tokens=tokens,
        top_n=top_n,
        output_path=output_dir / "sandra_top_tokens.png",
        title=f"Top {top_n} Tokens: {title}",
        LOG=LOG,
    )

    # ============================================================
    # PHASE 4.2: Word cloud
    # ============================================================

    LOG.info("========================")
    LOG.info("PHASE 4.2: Word cloud")
    LOG.info("========================")

    _plot_wordcloud(
        text=tokens_str,
        output_path=output_dir / "sandra_wordcloud.png",
        title=f"Word Cloud: {title}",
        LOG=LOG,
    )

    # ============================================================
    # PHASE 4.3: Token length histogram
    # ============================================================

    LOG.info("========================")
    LOG.info("PHASE 4.3: Token length histogram")
    LOG.info("========================")

    _plot_token_length_histogram(
        tokens=tokens,
        output_path=output_dir / "sandra_token_length_histogram.png",
        title=f"Token Length Distribution: {title}",
        LOG=LOG,
    )

    # ============================================================
    # PHASE 4.4: Inline token summary
    # ============================================================

    LOG.info("========================")
    LOG.info("PHASE 4.4: Top token summary (inline)")
    LOG.info("========================")

    counter = Counter(tokens)
    top_tokens = counter.most_common(top_n)

    LOG.info(f"Top {top_n} tokens by frequency:")
    for rank, (word, count) in enumerate(top_tokens, start=1):
        LOG.info(f"{rank:>2}. {word:<25} {count}")

    LOG.info("Sink: visualizations saved to data/processed/")
    LOG.info("Analysis complete.")
