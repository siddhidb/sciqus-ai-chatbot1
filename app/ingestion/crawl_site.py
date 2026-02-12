# app/ingestion/crawl_site.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def crawl_website(base_url: str, max_pages: int = 200):
    """
    Crawl a website and return extracted page text.

    Returns:
        List[dict]: [{ "url": str, "text": str }]
    """

    visited = set()
    to_visit = [base_url]
    pages = []

    base_domain = urlparse(base_url).netloc

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)

        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except Exception:
            continue

        visited.add(url)

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove noisy elements
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        if text:
            pages.append({
                "url": url,
                "text": text
            })

        # Discover internal links
        for link in soup.find_all("a", href=True):
            href = link["href"]
            next_url = urljoin(url, href)
            parsed = urlparse(next_url)

            if parsed.netloc == base_domain and next_url not in visited:
                to_visit.append(next_url)

    return pages
