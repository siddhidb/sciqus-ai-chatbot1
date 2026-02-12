import json
import os
from datetime import datetime

BASE_DIR = os.getenv("SCIQUS_DATA_DIR") or os.path.join(os.path.abspath(os.sep), "tmp")
SOURCES_FILE = os.path.join(BASE_DIR, "sciqus_sources.json")


def _load_sources():
    if not os.path.exists(SOURCES_FILE):
        return []
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_sources(data):
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def register_source(source_name: str, source_type: str, location: str):
    sources = _load_sources()

    # prevent duplicate registration
    if any(s["source_name"] == source_name for s in sources):
        return

    sources.append({
        "source_name": source_name,
        "type": source_type,     # pdf | website | doc
        "location": location,    # file path or URL
        "created_at": datetime.utcnow().isoformat()
    })

    _save_sources(sources)
    print(f"📚 Source registered: {source_name}")


def list_sources():
    return _load_sources()


def remove_source(source_name: str):
    sources = _load_sources()
    updated = [s for s in sources if s["source_name"] != source_name]

    if len(updated) == len(sources):
        return False

    _save_sources(updated)
    print(f"🗑️ Source removed: {source_name}")
    return True
