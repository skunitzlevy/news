import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

NYTIMES_URL = "https://www.nytimes.com/"
ARTICLE_PATH_PATTERN = re.compile(r"/\d{4}/\d{2}/\d{2}/.+\.html$")


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


def main():
    for header in get_article_headers():
        print(header)


if __name__ == "__main__":
    main()
