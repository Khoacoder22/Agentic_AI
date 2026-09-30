from src.chains.agentic_rag import agentic_rag


question = input("Enter your question: ")

answer = agentic_rag(question)

print("\nFINAL ANSWER:")
print(answer)