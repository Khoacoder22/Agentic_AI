import json

from src.chains.llm import ask_llm
from src.retrieval.retriever import retrieve
from src.prompts.prompts import (
    AGENT_DECISION_PROMPT,
    SELF_CHECK_PROMPT
)


MAX_ROUNDS = 3


def decide_action(question, context):

    prompt = AGENT_DECISION_PROMPT.format(
        question=question,
        context=context
    )

    response = ask_llm(prompt)

    return json.loads(response)


def generate_answer(question, context):
    prompt = f"""
Answer the question using only the context below.

Question:
{question}

Context:
{context}

Rules:
- Use only the provided context.
- Answer the exact question.
- If the question asks "Who", provide the person's name when available.
- Do not replace a person's name with a team, department, or role.
- Do not invent information.
- If the answer is not supported by the context,
  say "I don't know".
- You MUST include a citation after the factual answer.
- Copy the citation exactly from the context.
- Citation format: [source:chunk_id]

Example:
John leads the backend engineering team. [departments:01]

Return only the final answer.
"""
    return ask_llm(prompt)


def self_check(question, answer, context):

    prompt = SELF_CHECK_PROMPT.format(
        question=question,
        answer=answer,
        context=context
    )

    response = ask_llm(prompt)

    return json.loads(response)


def agentic_rag(question):

    context = []

    # PHASE 1: AGENT RETRIEVAL

    retrieved_queries = []

    for round_number in range(MAX_ROUNDS):
        context_text = "\n\n".join(
            item["text"]
            for item in context
        )

        decision = decide_action(question, context_text)

        print(f"\n--- Agent Round {round_number + 1} ---")
        print("Decision:", decision)

        if decision["action"] == "answer":
            break

        query = decision["query"].strip()

        # Avoid retrieving the same query repeatedly
        if query.lower() in [q.lower() for q in retrieved_queries]:
            print("Repeated query detected. Stopping retrieval.")
            break

        retrieved_queries.append(query)

        print("Retrieving:", query)

        results = retrieve(query, top_k=3)
        context.extend(results)

    # PHASE 2: GENERATE ANSWER

    context_text = "\n\n".join(
        item["text"]
        for item in context
    )

    answer = generate_answer(
        question,
        context_text
    )

    print("\nGenerated answer:")
    print(answer)

    # PHASE 3: SELF-CHECK

    check = self_check(
        question,
        answer,
        context_text
    )

    print("\nSelf-check:")
    print(check)

    # Answer is supported
    if check["supported"]:
        return answer

    # PHASE 4: RETRIEVE MISSING INFO

    missing = check.get(
        "missing_information",
        question
    )

    print("\nMissing information:")
    print(missing)

    extra_results = retrieve(
        missing,
        top_k=3
    )

    context.extend(extra_results)

    # PHASE 5: FINAL ANSWER

    context_text = "\n\n".join(
        item["text"]
        for item in context
    )

    final_answer = generate_answer(
        question,
        context_text
    )

    return final_answer