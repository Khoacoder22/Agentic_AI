from src.retrieval.retriever import retrieve
from src.chains.llm import ask_llm
from src.prompts.prompts import NAIVE_RAG_PROMPT

def naive_rag(question: str):

    results = retrieve(question, top_k=3)

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    prompt = NAIVE_RAG_PROMPT.format(
        context=context,
        question=question
    )

    answer = ask_llm(prompt)

    return {
        "answer": answer,
        "retrieved": results
    }