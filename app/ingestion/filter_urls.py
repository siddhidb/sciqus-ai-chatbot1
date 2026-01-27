from pathlib import Path

INPUT = Path("data/sciqusams_urls.txt")
OUTPUT = Path("data/sciqusams_urls_filtered.txt")

exclude_keywords = [
    "checkout",
    "wishlist",
    "purchase",
    "lp-",
    "user-account",
    "membership",
    "login",
    "restricted",
    "account",
    "elementor",
    "student",
    "instructor",
    "profile",
    "register"
]

filtered = []

for url in INPUT.read_text(encoding="utf-8").splitlines():
    if not any(k in url for k in exclude_keywords):
        filtered.append(url)

OUTPUT.write_text("\n".join(filtered), encoding="utf-8")

print(f"✅ Filtered URLs: {len(filtered)} (from original list)")
