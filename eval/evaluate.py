import json

from src.chains.naive_rag import naive_rag
from src.chains.agentic_rag import agentic_rag


def load_questions():

    with open(
        "eval/questions.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def check_answer(answer, expected):

    answer = answer.lower()
    expected = expected.lower()

    return expected in answer


def evaluate_naive(questions):

    correct = 0

    for i, item in enumerate(questions, start=1):

        question = item["question"]
        expected = item["answer"]

        print(f"\n[{i}/20] {question}")

        result = naive_rag(question)

        answer = result["answer"]

        is_correct = check_answer(
            answer,
            expected
        )

        if is_correct:
            correct += 1

        print("Expected:", expected)
        print("Answer:", answer)
        print("Correct:", is_correct)

    return correct


def evaluate_agentic(questions):

    correct = 0

    for i, item in enumerate(questions, start=1):

        question = item["question"]
        expected = item["answer"]

        print(f"\n[{i}/20] {question}")

        answer = agentic_rag(question)

        is_correct = check_answer(
            answer,
            expected
        )

        if is_correct:
            correct += 1

        print("Expected:", expected)
        print("Answer:", answer)
        print("Correct:", is_correct)

    return correct


questions = load_questions()

print("NAIVE RAG EVALUATION")

naive_correct = evaluate_naive(
    questions
)


print("AGENTIC RAG EVALUATION")

agentic_correct = evaluate_agentic(
    questions
)


naive_accuracy = (
    naive_correct / len(questions)
)

agentic_accuracy = (
    agentic_correct / len(questions)
)
print("FINAL RESULTS")

print(
    f"Naive RAG: "
    f"{naive_correct}/20 "
    f"({naive_accuracy:.1%})"
)

print(
    f"Agentic RAG: "
    f"{agentic_correct}/20 "
    f"({agentic_accuracy:.1%})"
)


if naive_accuracy > 0:

    improvement = (
        (agentic_accuracy - naive_accuracy)
        / naive_accuracy
        * 100
    )

    print(
        f"Improvement: "
        f"{improvement:.2f}%"
    )