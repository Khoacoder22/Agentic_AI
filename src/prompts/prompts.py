# NATVIE RAG
NAIVE_RAG_PROMPT = """
Answer the question using only the context below.

Context:
{context}

Question:
{question}

Rules:
- Use only the provided context.
- Do not invent information.
- If the answer is not supported by the context,
  say "I don't know".
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
2. If the answer is "I don't know" but the context actually contains
   the information needed to answer the question, return supported=false.
3. If the answer is incomplete or does not answer the question,
   return supported=false.
4. Only return supported=true when the answer correctly answers the
   question using information explicitly present in the context.

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