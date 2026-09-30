from src.chains.naive_rag import naive_rag
from src.chains.agentic_rag import agentic_rag

while True:
    question = input("question(type exist if you want out): ")
    if question.lower() == 'exist':
        break

    answer = agentic_rag(question)
    
    print("\nAnswer:")
    print(answer)