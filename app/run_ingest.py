from app.ingestion.ingest import ingest_website

print("🚀 Starting website ingestion...")

ingest_website(
    base_url="https://sciqusams.com",
    source_name="sciqus_website"
)

print("✅ Website ingestion completed successfully")
