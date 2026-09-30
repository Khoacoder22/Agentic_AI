from src.retrieval.retriever import retrieve


question = "What database does Larry corp use?"

results = retrieve(
    question,
    top_k=3
)

print("QUESTION:")
print(question)

print("\nRESULTS:")

for i, result in enumerate(results, start=1):

    print(f"\n--- Result {i} ---")
    print("Source:", result["source"])
    print("Score:", result["score"])
    print("Text:", result["text"])