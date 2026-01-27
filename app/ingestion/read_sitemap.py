import requests
import xml.etree.ElementTree as ET

SITEMAP_URL = "https://sciqusams.com/sitemap-1.xml"

response = requests.get(SITEMAP_URL, timeout=10)
response.raise_for_status()

root = ET.fromstring(response.text)

# XML namespace used in sitemaps
ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

urls = []

for url in root.findall("ns:url", ns):
    loc = url.find("ns:loc", ns)
    if loc is not None:
        urls.append(loc.text.strip())

with open("data/sciqusams_urls.txt", "w", encoding="utf-8") as f:
    for u in urls:
        f.write(u + "\n")

print(f"✅ Extracted {len(urls)} URLs from sitemap")
