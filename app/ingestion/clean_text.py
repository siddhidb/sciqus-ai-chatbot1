from bs4 import BeautifulSoup
from pathlib import Path

RAW = Path("data/raw")
OUT = Path("data/cleaned")
OUT.mkdir(exist_ok=True)

for file in RAW.glob("*.html"):
    soup = BeautifulSoup(file.read_text(), "html.parser")
    for tag in soup(["nav","footer","script","style"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    (OUT / file.name.replace(".html",".txt")).write_text(text)
