# Agentic RAG

## Introduction

This project is a simple Agentic RAG chatbot built from scratch with
Python and Azure OpenAI.

The knowledge base contains several `.txt` files about Larry corp. The
system supports both Naive RAG and Agentic RAG so their results can be
compared.

## Project Flow

### Build Index

``` text
TXT files
   ↓
Load documents
   ↓
Split into chunks
   ↓
Create embeddings
   ↓
Save to JSON vector store
```

Run:

``` bash
python build_index.py
```

### Naive RAG

``` text
Question
   ↓
Retrieve top 3 chunks
   ↓
Send context + question to LLM
   ↓
Answer
```

### Agentic RAG

``` text
Question
   ↓
Retrieve information
   ↓
Agent checks the context
   ↓
Enough information?
   ├── Yes → Generate answer → Self-check
   └── No  → Create new query → Retrieve again
```

This allows the agent to handle questions that require information from
multiple chunks.

## Citation

Retrieved chunks have a source and chunk ID:

``` text
[employees:01]
Larry is the CEO of Larry corp.
```

The answer can use the same citation:

``` text
Larry is the CEO of Larry corp. [employees:01]
```

## Evaluation

The system was tested with 20 questions.

  System             Accuracy
  ------------- -------------
  Naive RAG       14/20 (70%)
  Agentic RAG     17/20 (85%)

Improvement: **21.43%**

## Reflection

Agentic RAG works better when a question needs information from more
than one chunk. It can decide that the current information is not enough
and retrieve again with a more specific query. This helps with multi-hop
questions. In my experiment, Agentic RAG got 85% accuracy while Naive
RAG got 70%. However, Agentic RAG needs more LLM calls, so it can take
more time and cost more.
