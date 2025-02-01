from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# ✅ Connect to Qdrant Server
qdrant = QdrantClient("http://localhost:6333")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
COLLECTION_NAME = "research_papers"

def search_papers(query, top_k=3):
    """
    Searches for research papers in Qdrant based on similarity.
    """
    query_vector = embedding_model.encode(query).tolist()

    search_results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )

    results = []
    for hit in search_results:
        paper = hit.payload
        results.append({
            "title": paper["title"],
            "authors": paper["authors"],
            "summary": paper["summary"],
            "pdf_url": paper["pdf_url"],
            "published": paper["published"],
            "score": hit.score
        })

    return results

if __name__ == "__main__":
    query = "Explain GPT models"
    results = search_papers(query)

    for i, paper in enumerate(results):
        print(f"\n🔹 Result {i+1}: {paper['title']} (Score: {paper['score']:.4f})")
        print(f"   📅 Published: {paper['published']}")
        print(f"   ✍️ Authors: {', '.join(paper['authors'])}")
        print(f"   📄 PDF: {paper['pdf_url']}")
        print(f"   🔍 Summary: {paper['summary'][:500]}...\n")
