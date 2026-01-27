import requests
from bs4 import BeautifulSoup
from pathlib import Path

BASE_URL = "https://sciqus.com/ams"
OUT = Path("data/raw")
OUT.mkdir(parents=True, exist_ok=True)

def crawl(url):
    html = requests.get(url, timeout=10).text
    name = url.replace("/", "_").replace(":", "")
    (OUT / f"{name}.html").write_text(html, encoding="utf-8")

crawl(BASE_URL)
