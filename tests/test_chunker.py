from src.loaders.text_loader import load_directory
from src.chunkers.text_chunker import chunk_text


documents = load_directory("data/raw")

for document in documents:

    print("SOURCE:", document["source"])

    chunks = chunk_text(
        document["text"],
        chunk_size=20,
        overlap=5
    )

    for i, chunk in enumerate(chunks):
        print(f"CHUNK {i + 1}:")
        print(chunk)
        print("--------------------")