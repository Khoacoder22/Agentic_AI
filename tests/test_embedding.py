from src.embeddings.azure_embedding import create_embedding


text = "Larry corp is a software company."

vector = create_embedding(text)

print("Vector type:", type(vector))
print("Vector length:", len(vector))
print("First 10 values:", vector[:10])