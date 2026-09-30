def chunk_text( text: str, chunk_size: int = 100, overlap: int = 20 ): 
    # splitting text
    words = text.split()

    chunks = []

    start = 0
    chunk_index = 1

    while start < len(words):
        end = start + chunk_size

        chunk = " ".join(
            words[start:end]
        )

        chunks.append({
            "chunk_id" : f"{chunk_index:02d}",
            "text": " ".join(words[start:end])
        })

        chunk_index += 1
        start += chunk_size - overlap

    return chunks