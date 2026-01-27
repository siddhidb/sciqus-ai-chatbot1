import requests
from bs4 import BeautifulSoup
from pathlib import Path

URL_FILE = "data/sciqusams_urls_filtered.txt"
OUTPUT_DIR = Path("data/raw")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

urls = URL_FILE
urls = open(urls, encoding="utf-8").read().splitlines()

for url in urls:
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove non-content elements
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "noscript",
            "form"
        ]):
            tag.decompose()

        text = soup.get_text(separator="\n")

        filename = url.replace("https://", "").replace("/", "_") + ".txt"
        (OUTPUT_DIR / filename).write_text(text, encoding="utf-8")

        print(f"✅ Extracted: {url}")

    except Exception as e:
        print(f"❌ Failed: {url} | {e}")
