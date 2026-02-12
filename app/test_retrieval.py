from app.core.retrieval import retrieve_context

if __name__ == "__main__":
    results = retrieve_context("What is sciqus ams", top_k=3)

    print("\n--- RETRIEVAL RESULTS ---\n")
    for i, r in enumerate(results, start=1):
        print(f"Result {i}:")
        print(r["content"])
        print("-" * 50)
