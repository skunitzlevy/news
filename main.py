import re
import textwrap
from urllib.parse import urlparse

import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

from hf_test import classify_headline, print_headline_sentiment

NYTIMES_URL = "https://www.nytimes.com/"
ARTICLE_PATH_PATTERN = re.compile(r"/\d{4}/\d{2}/\d{2}/.+\.html$")
CHART_PATH = "sentiment_chart.png"


def get_article_headers(url=NYTIMES_URL):
    """Return the article headers found on a New York Times page."""
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; news-scraper/1.0)"},
        timeout=10,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    headers = []
    seen = set()

    for link in soup.select("main a[href]"):
        if not ARTICLE_PATH_PATTERN.search(urlparse(link["href"]).path):
            continue

        headline = link.select_one('.indicate-hover, [class*="headline"]')
        if headline is None:
            continue

        header = headline.get_text(" ", strip=True)
        if header and header not in seen:
            headers.append(header)
            seen.add(header)

    return headers


def create_sentiment_chart(classifications, output_path=CHART_PATH):
    """Save a horizontal stacked chart of sentiment scores by headline."""
    labels = [textwrap.shorten(headline, width=72) for headline, _ in classifications]
    scores = [
        {result["label"].lower(): result["score"] for result in results}
        for _, results in classifications
    ]

    figure_height = max(6, len(labels) * 0.42)
    figure, axis = plt.subplots(figsize=(13, figure_height))
    left = [0.0] * len(labels)

    colors = {
        "negative": "#d95f5f",
        "neutral": "#9aa0a6",
        "positive": "#55a868",
    }

    for sentiment in ("negative", "neutral", "positive"):
        values = [score.get(sentiment, 0.0) for score in scores]
        axis.barh(
            labels, values, left=left, label=sentiment.title(), color=colors[sentiment]
        )
        left = [start + value for start, value in zip(left, values)]

    axis.set_title("New York Times Headline Sentiment")
    axis.set_xlabel("Model confidence")
    axis.set_xlim(0, 1)
    axis.invert_yaxis()
    axis.legend(loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=3, frameon=False)
    axis.grid(axis="x", alpha=0.2)
    figure.tight_layout()
    figure.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(figure)

    return output_path


def main():
    classifications = []

    for header in get_article_headers():
        results = classify_headline(header)
        classifications.append((header, results))
        print_headline_sentiment(header, results)

    chart_path = create_sentiment_chart(classifications)
    print(f"Saved sentiment chart to {chart_path}")


if __name__ == "__main__":
    main()
