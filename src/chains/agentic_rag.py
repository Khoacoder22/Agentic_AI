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
- Identify the source chunk that directly supports the answer.
- Only use citation IDs that actually appear in the context.

Return JSON only:

{{
    "answer": "your answer",
    "citations": ["source:chunk_id"]
}}
"""

    response = ask_llm(prompt)

    return json.loads(response)


def validate_citations(result, context):

    valid_citations = []

    for item in context:

        citation = (
            f"{item['source'].replace('.txt', '')}:{item['chunk_id']}"
        )

        valid_citations.append(citation)

    valid_result = []

    for citation in result.get("citations", []):

        if citation in valid_citations:
            valid_result.append(citation)

    result["citations"] = valid_result

    return result


def format_answer(result):

    answer = result["answer"]

    citations = result.get("citations", [])

    if citations:

        citation_text = " ".join(
            f"[{citation}]"
            for citation in citations
        )

        return f"{answer} {citation_text}"

    return answer


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

    # AGENT RETRIEVAL

    retrieved_queries = []

    for round_number in range(MAX_ROUNDS):

        context_text = "\n\n".join(
            f"[{item['source'].replace('.txt', '')}:{item['chunk_id']}]\n"
            + item["text"]
            for item in context
        )

        decision = decide_action(
            question,
            context_text
        )

        print(f"\n--- Agent Round {round_number + 1} ---")
        print("Decision:", decision)

        if decision["action"] == "answer":
            break

        query = decision["query"].strip()

        # Avoid retrieving the same query repeatedly
        if query.lower() in [
            q.lower() for q in retrieved_queries
        ]:
            print("Repeated query detected. Stopping retrieval.")
            break

        retrieved_queries.append(query)

        print("Retrieving:", query)

        results = retrieve(
            query,
            top_k=3
        )

        context.extend(results)

    # GENERATE ANSWER

    context_text = "\n\n".join(
        f"[{item['source'].replace('.txt', '')}:{item['chunk_id']}]\n"
        + item["text"]
        for item in context
    )

    answer_result = generate_answer(
        question,
        context_text
    )

    # Validate citation IDs
    answer_result = validate_citations(
        answer_result,
        context
    )

    # Convert JSON result -> final text
    answer = format_answer(answer_result)

    print("\nGenerated answer:")
    print(answer)

    # SELF-CHECK

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

    # RETRIEVE MISSING INFO

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

    # FINAL ANSWER

    context_text = "\n\n".join(
        f"[{item['source'].replace('.txt', '')}:{item['chunk_id']}]\n"
        + item["text"]
        for item in context
    )

    final_result = generate_answer(
        question,
        context_text
    )

    final_result = validate_citations(
        final_result,
        context
    )

    final_answer = format_answer(
        final_result
    )

    return final_answer