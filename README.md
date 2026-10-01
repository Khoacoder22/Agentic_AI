# Agentic RAG Chatbot

## 1. Project Overview

This project implements an **Agentic Retrieval-Augmented Generation

(RAG)** chatbot from scratch.

The main goal is to compare a traditional **Naive RAG** pipeline with an

**Agentic RAG** pipeline. The system uses a small company knowledge base

stored as text files. Documents are manually chunked, converted into

embeddings, stored in a JSON-based vector store, and retrieved using

cosine similarity.

The Agentic RAG system extends the standard RAG pipeline by allowing an

LLM-based retrieval agent to:

-   Decide whether the current context is sufficient.

-   Generate a new retrieval query when information is missing.

-   Perform multiple retrieval rounds.

-   Connect information from different chunks or documents.

-   Perform a self-check before returning the answer.

The project is intentionally implemented without LangChain, Chroma,

FAISS, or other RAG frameworks in order to understand the internal RAG

flow.

------------------------------------------------------------------------

## 2. Main Technologies

-   Python

-   Azure OpenAI

-   `gpt-5.6-luna` for LLM reasoning and answer generation

-   `text-embedding-3-small` for embeddings

-   NumPy for cosine similarity

-   JSON for the hand-rolled vector store

------------------------------------------------------------------------

## 3. Project Structure

``` text

C:\RAG_chat

│

├── data/

│   ├── raw/

│   │   ├── company.txt

│   │   ├── infrastructure.txt

│   │   ├── employees.txt

│   │   ├── products.txt

│   │   ├── projects.txt

│   │   ├── departments.txt

│   │   └── security.txt

│   │

│   └── processed/

│       └── vector_store.json

│

├── src/

│   ├── loaders/

│   │   └── text_loader.py

│   │

│   ├── chunkers/

│   │   └── text_chunker.py

│   │

│   ├── embeddings/

│   │   └── azure_embedding.py

│   │

│   ├── vector_store/

│   │   └── json_store.py

│   │

│   ├── retrieval/

│   │   └── retriever.py

│   │

│   ├── chains/

│   │   ├── llm.py

│   │   ├── naive_rag.py

│   │   └── agentic_rag.py

│   │

│   └── prompts/

│       └── prompts.py

│

├── eval/

│   ├── questions.json

│   └── evaluate.py

│

├── build_index.py

├── ask.py

├── .env

├── .env.example

├── .gitignore

├── pyproject.toml

└── README.md

```

------------------------------------------------------------------------

# 4. Knowledge Base

The knowledge base contains several `.txt` files describing Larry corp.

Examples:

-   `company.txt` contains company information.

-   `infrastructure.txt` contains AWS, PostgreSQL, Redis, and backend

    infrastructure information.

-   `employees.txt` contains employee roles.

-   `products.txt` contains QueuePro information.

-   `projects.txt` contains Project Alpha and Project Beta.

-   `departments.txt` contains department responsibilities.

-   `security.txt` contains authentication information.

The raw documents are located in:

``` text

data/raw/

```

------------------------------------------------------------------------

# 5. Indexing Flow

Before the RAG system can retrieve information, the raw documents must

be converted into searchable vectors.

The indexing process is:

``` text

Raw TXT Documents

       |

       v

Text Loader

       |

       v

Text Chunking

       |

       v

Create Embeddings

       |

       v

JSON Vector Store

```

## Step 1: Load documents

`text_loader.py` reads all `.txt` files from `data/raw/`.

Each document contains:

``` python

{

    "source": "employees.txt",

    "text": "Larry is the CEO of Larry corp..."

}

```

## Step 2: Chunk documents

`text_chunker.py` splits a document into smaller chunks.

Each chunk receives a `chunk_id`:

``` json

{

    "chunk_id": "01",

    "text": "Larry is the CEO of Larry corp."

}

```

The current indexing configuration uses:

``` text

chunk_size = 20 words

overlap = 5 words

```

The overlap helps preserve information between neighboring chunks.

## Step 3: Create embeddings

Each chunk is sent to the Azure OpenAI embedding deployment:

``` text

text-embedding-3-small

```

The resulting vector represents the semantic meaning of the chunk.

## Step 4: Save the vector store

The chunk text, source, chunk ID, and embedding are stored in:

``` text

data/processed/vector_store.json

```

Run the indexing process with:

``` powershell

python build_index.py

```

Whenever the raw documents or chunking logic changes, rebuild the index

before running evaluation.

------------------------------------------------------------------------

# 6. Retrieval Flow

The retriever uses cosine similarity to compare the query embedding with

every stored chunk embedding.

``` text

User Question
      |
      v
Create Query Embedding

      |
      v
Compare with Stored Embeddings
      |
      v
Cosine Similarity
      |
      v
Sort by Similarity

      |
      v
Top-K Chunks

```

The current system uses:

``` python

retrieve(question, top_k=3)

```

Therefore, the retriever returns the three chunks with the highest

cosine similarity scores.

A retrieved chunk contains:

``` python

{

    "chunk_id": "01",

    "text": "...",

    "source": "employees.txt",

    "score": 0.91

}

```

------------------------------------------------------------------------

# 7. Citation System

Each retrieved chunk has a source and a chunk ID.

The RAG context is formatted like:

[employees:01]
Larry is the CEO of Larry corp.

[company:01]
Larry corp is a software company.

The citation format is:

[source:chunk_id]

For example:

Larry is the CEO of Larry corp. [employees:01]

For Agentic RAG, the LLM does not directly write the final citation into the
answer text. Instead, it returns a structured JSON result:

{
    "answer": "Larry is the CEO of Larry corp.",
    "citations": ["employees:01"]
}


This prevents the model from inventing citations such as
[source:context] that do not exist in the retrieved context.

The final formatted answer becomes:

Larry is the CEO of Larry corp. [employees:01]

# 8. Naive RAG Flow

Naive RAG performs retrieval only once.

``` text

User Question

      |

      v

Retrieve Top-3 Chunks

      |

      v

Build Context

      |

      v

LLM

      |

      v

Final Answer

```

The implementation is:

``` python

results = retrieve(question, top_k=3)

context = ...

prompt = NAIVE_RAG_PROMPT.format(

    context=context,

    question=question

)

answer = ask_llm(prompt)

```

The main limitation is that the system does not decide whether the first

retrieval contains all information required to answer a complex

question.

------------------------------------------------------------------------

# 9. Agentic RAG Flow

Agentic RAG introduces an agent loop that decides whether more retrieval is
required.

The main flow is:

                    User Question
                          |
                          v
                   Agent Decision
                          |
                    +-----+-----+
                    |           |
              Retrieve More    Enough
                    |           |
                    v           v
              New Query       Generate
                    |           |
                    v           v
                 Retrieve     JSON Answer
                    |           |
                    +-----> Validate Citations
                                   |
                                   v
                              Self-Check
                                   |
                              +----+----+
                              |         |
                          Supported   Not Supported
                              |         |
                              v         v
                           Return    Retrieve
                           Answer    Missing Info
                                         |
                                         v
                                  Generate Final Answer

The agent can return:

{
    "action": "retrieve",
    "query": "specific missing information"
}

or:

{
    "action": "answer"
}

The retrieval loop is limited by:

MAX_ROUNDS = 3

This prevents the agent from continuously retrieving information.

Structured Answer Generation

After retrieval, the answer-generation step returns JSON rather than plain
text:

{
    "answer": "Anna is responsible for the DevOps work on Project Beta.",
    "citations": ["projects:02"]
}

The Python code then:

Checks whether each citation exists in the retrieved context.

Removes invalid citation IDs.

Formats the answer with validated citations.

Sends the formatted answer to the self-check step.

This makes citation handling deterministic instead of relying completely on
the LLM to generate citation text correctly.

# 10. Multi-Hop Example

A multi-hop question is:

``` text

Who is responsible for the DevOps work on the project that stores files using Amazon S3?

```

The answer is not necessarily obtained from one simple fact.

The agent can perform multiple retrieval steps:

``` text

Round 1

Question:

Who is responsible for the DevOps work on the project that stores files using Amazon S3?

        |

        v

Retrieve information about the project using Amazon S3

        |

        v

Project Beta uses Amazon S3

```

Then the agent retrieves more information:

``` text

Round 2

Who is responsible for the DevOps work on Project Beta?

        |

        v

Anna is responsible for Project Beta DevOps

```

Finally, the system generates:

``` text

Anna is responsible for the DevOps work. [projects:...]

```

This demonstrates why iterative retrieval is useful for questions where

the required information is distributed across multiple facts.

------------------------------------------------------------------------

# 11. Agent Self-Check

After generating an answer, the Agentic RAG system performs a self-check.

Retrieved Context
       |
       v
Generate Structured Answer
       |
       v
Validate Citations
       |
       v
Format Answer
       |
       v
Self-Check
       |
    +--+--+
    |     |
Supported  Not Supported
    |          |
    v          v
 Return    Retrieve Missing Info
 Answer         |
                v
          Generate Final Answer

The self-check verifies whether the answer is supported by the retrieved
context.

It checks cases such as:

Information is missing.

The answer is incomplete.

The answer does not directly answer the question.

The answer contains an unsupported claim.

A citation does not refer to an actual retrieved chunk.

A question asking "Who" is answered with a role or department instead of
the person's name.

If the answer is not supported, the system uses the missing-information
description from the self-check as a new retrieval query and generates the
answer again using the expanded context.

# 12. Running the Project

## Build the index

``` powershell

python build_index.py

```

## Run the evaluation

``` powershell

python -m eval.evaluate

```

## Ask your own questions

The project also supports interactive questions through:

``` powershell

python ask.py

```

Example:

``` text

You: Who is the CEO of Larry corp?

```

The Agentic RAG pipeline then performs retrieval, reasoning, answer

generation, and self-checking.

------------------------------------------------------------------------

# 13. Evaluation

The project contains 20 evaluation questions.

The evaluation compares:

``` text

Naive RAG

vs.

Agentic RAG

```

Current evaluation result:

  System          Correct   Accuracy

**  ------------- --------- ----------**

  Naive RAG         14/20        70%

  Agentic RAG       18/20        90%

Relative improvement:

``` text

28.57%

```

Therefore, the Agentic RAG system exceeds the required 20% improvement

over the Naive RAG baseline in the current evaluation run.

------------------------------------------------------------------------

# 14. English Reflection

Agentic RAG performs better when a question requires multiple retrieval

steps to connect different pieces of information. Unlike naive RAG, the

agent can identify missing information and generate a more specific

retrieval query. This is especially useful for multi-hop questions where

the answer is distributed across different documents or chunks. The

agent can also check whether the retrieved context is sufficient before

generating the final answer. In our evaluation, Agentic RAG achieved 90%

accuracy compared with 70% for Naive RAG, which represents a 28.57%

relative improvement. 

------------------------------------------------------------------------

# 15. Summary of the Complete System

The complete project flow is:

                     OFFLINE INDEXING

Raw TXT Documents
        |
        v
Load Documents
        |
        v
Chunk Text
        |
        v
Create Embeddings
        |
        v
JSON Vector Store


                     ONLINE QUERY

User Query
        |
        v
Agent Decision
        |
        +----------------------+
        |                      |
        v                      v
Retrieve More              Generate Answer
        |                      |
        v                      v
Create Query Embedding    Validate Citations
        |                      |
        v                      v
Vector Retrieval          Format Answer
        |                      |
        +----------+-----------+
                   |
                   v
               Self-Check
                   |
              +----+----+
              |         |
          Supported   Not Supported
              |         |
              v         v
           Return    Retrieve Missing
           Answer       Information
                            |
                            v
                    Generate Final Answer

The main difference is that Naive RAG retrieves once and generates an
answer, while Agentic RAG can decide what information is still missing,
retrieve again, connect information from multiple chunks, validate citations,
and perform a self-check before returning the answer.

