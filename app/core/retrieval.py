# from app.core.vectorstore import get_collection

# def retrieve_context(query: str, top_k: int = 5) -> list[str]:
#     collection = get_collection()

#     results = collection.query(
#         query_texts=[query],
#         n_results=top_k
#     )

#     docs = results.get("documents", [[]])[0]

#     clean_docs = [
#         d.strip()
#         for d in docs
#         if d and len(d.strip()) > 80
#     ]

#     return clean_docs
from app.core.vectorstore import get_collection

def retrieve_context(query: str, top_k: int = 5) -> list[str]:
    collection = get_collection()

    count = collection.count()
    if count == 0:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, count)
    )

    documents = results.get("documents", [[]])[0]

    return [
        d.strip()
        for d in documents
        if isinstance(d, str) and len(d.strip()) > 80
    ]
