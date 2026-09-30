import numpy as np 

from src.embeddings.azure_embedding import create_embedding
from src.vector_store.json_store import load_vectors

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    denominator = (np.linalg.norm(a) * np.linalg.norm(b))

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b)/ denominator)

def retrieve(query: str, top_k: int = 3):
    query_embedding = create_embedding(query)

    # Load stored vectors
    documents = load_vectors()
    results = []

    # compare question vector 
    for document in documents: 

        score = cosine_similarity(query_embedding, document["embedding"])

        results.append({
            "text" : document["text"],
            "source": document["source"],
            "score": score
        })

    # Highest similarity first
    results.sort(key=lambda x: x["score"], reverse= True)

    # Return top K 
    return results[:top_k]