from src.chains.naive_rag import naive_rag


question = input("Enter your question: ")

result = naive_rag(question)


print("\nANSWER:")
print(result["answer"])


print("\nRETRIEVED DOCUMENTS:")

for item in result["retrieved"]:

    print("\nSource:", item["source"])
    print("Score:", item["score"])
    print("Text:", item["text"])