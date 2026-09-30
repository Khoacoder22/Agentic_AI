from src.loaders.text_loader import load_directory
from src.chunkers.text_chunker import chunk_text
from src.embeddings.azure_embedding import create_embedding
from src.vector_store.json_store import save_vectors

documents = load_directory("data/raw")

all_chunks = []

for document in documents: 

    chunks = chunk_text(
        document["text"],
        chunk_size=20,
        overlap=5
    )

    for chunk in chunks: 

        embedding = create_embedding(chunk["text"])

        all_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "source": document["source"],
            "embedding": embedding
        })

save_vectors(all_chunks)

print(f"Created {len(all_chunks)} chunks.")
print("Vector store saved successfully.")