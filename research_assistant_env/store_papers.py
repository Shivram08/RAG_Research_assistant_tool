from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
from sentence_transformers import SentenceTransformer
import uuid

# ✅ Connect to Qdrant Server
qdrant = QdrantClient("http://localhost:6333")  # Use Qdrant server

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
COLLECTION_NAME = "research_papers"

# Create collection in Qdrant
qdrant.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # Adjust based on model
)

def store_papers_in_qdrant(papers):
    """
    Stores research papers in Qdrant with embeddings.
    """
    vectors = []
    for paper in papers:
        paper_text = f"{paper['title']} {paper['summary']}"
        embedding = embedding_model.encode(paper_text).tolist()

        vectors.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "title": paper["title"],
                    "authors": paper["authors"],
                    "summary": paper["summary"],
                    "pdf_url": paper["pdf_url"],
                    "published": paper["published"]
                }
            )
        )

    # ✅ Insert data into Qdrant
    qdrant.upsert(collection_name=COLLECTION_NAME, points=vectors)
    print(f"✅ Stored {len(vectors)} papers in Qdrant Server.")

if __name__ == "__main__":
    from fetch_papers import fetch_research_papers
    topic = '("Large Language Models" OR "LLM") AND ("Transformer" OR "GPT" OR "Deep Learning")'
    papers = fetch_research_papers(topic, max_results=10)
    
    store_papers_in_qdrant(papers)
