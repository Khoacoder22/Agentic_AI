# NAIVE RAG
NAIVE_RAG_PROMPT = """
Answer the question using only the context below.

Context:
{context}

Question:
{question}

Rules:
- Use only the provided context.
- Answer the exact question.
- If the question asks "Who", provide the person's name when available.
- Do not replace a person's name with a team, department, or role.
- Do not invent information.
- If the answer is not supported by the context,
  say "I don't know".
- Include a citation after the factual answer.
- Copy the citation exactly from the context.
- Citation format: [source:chunk_id]

Example:
John leads the backend engineering team. [departments:01]

Return only the final answer.
"""


# AGENT DECISION
AGENT_DECISION_PROMPT = """
You are a retrieval agent.

Your job is to decide whether the current context contains
ENOUGH information to answer the question completely.

Question:
{question}

Current context:
{context}

Important rules:

1. Identify all facts required to answer the question.

2. If the question requires connecting multiple facts or entities,
   make sure ALL required connections are explicitly supported.

3. Do not assume that two facts are related just because they
   mention the same name.

4. If ANY required fact is missing, you MUST retrieve more information.

5. Only return "answer" when the complete answer is explicitly
   supported by the current context.

6. If the current context is insufficient, identify the specific
   missing fact and create a retrieval query focused on that fact.

7. Do not repeat a previous retrieval query.

8. If the question asks "Who", make sure the context identifies
   the person, not only a team, department, or role.

9. If the question asks for a person, do not consider a team,
   department, or role to be a complete answer.

If more information is needed, return exactly:

{{
    "action": "retrieve",
    "query": "the search query needed to find the missing information"
}}

If the context contains all required information, return exactly:

{{
    "action": "answer"
}}

Return JSON only.
Do not include markdown.
Do not explain your decision.
"""


# SELF CHECK
SELF_CHECK_PROMPT = """
Check whether the answer is fully supported by the provided context.

Question:
{question}

Answer:
{answer}

Context:
{context}

Important rules:

1. Check whether the context contains enough information to answer
   the question.

2. Check whether the answer directly answers the exact question.

3. If the answer is "I don't know" but the context actually contains
   the information needed to answer the question, return supported=false.

4. If the answer is incomplete or does not answer the question,
   return supported=false.

5. Only return supported=true when the answer correctly answers the
   question using information explicitly present in the context.

6. Check whether the citation in the answer exists in the provided
   context.

7. If the answer gives a factual answer but has no citation,
   return supported=false.

8. If the question asks "Who", the answer must provide a person's
   name when the person's name is available in the context.

9. Do not accept a team, department, or role as a replacement
   for a person's name.

10. Do not accept information that is only implied or assumed.
    The answer must be explicitly supported by the context.

Return JSON only.

If the answer is fully supported by the context:

{{
    "supported": true
}}

If the answer is NOT fully supported:

{{
    "supported": false,
    "missing_information": "describe what information is missing"
}}
"""