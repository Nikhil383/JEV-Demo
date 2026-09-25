# Support Ticket Decision Engine

## 1. Problem Statement

Customer support teams handle large numbers of tickets involving billing, technical issues, sales, and subscriptions. Manually classifying tickets, deciding urgency, finding relevant knowledge, and writing responses can be slow and inconsistent.

This project automates these steps using **Laya for decisions, RAG for knowledge retrieval, and Gemini for response generation**.

## 2. Introduction

The application accepts a customer ticket and follows this workflow:

```text
Customer Ticket
      ↓
Laya → Department, Urgency, Human Review
      ↓
RAG → Relevant Knowledge
      ↓
Gemini → Grounded Response
      ↓
Streamlit UI
```

This is a demonstration of a **JEV-style decision-model concept using Laya**. It does not implement JEV itself.

## 3. Tech Stack

| Technology | Usage |
|---|---|
| Python | Application development |
| uv | Package/environment management |
| Laya | Structured decisions |
| Gemini | Response generation |
| ChromaDB | Vector storage |
| Sentence Transformers | Text embeddings |
| Streamlit | Web UI |
| python-dotenv | Environment configuration |

## 4. Folder Structure

```text
laya-gemini-rag/
├── app.py
├── pyproject.toml
├── uv.lock
├── .env
├── .env.example
├── data/
│   └── knowledge/
│       ├── refunds.md
│       ├── billing.md
│       ├── technical.md
│       └── subscriptions.md
└── src/
    ├── config.py
    ├── rag.py
    ├── laya_engine.py
    └── gemini.py
```

## 5. Steps to Execute the Project

### Install dependencies

```bash
uv sync
```

### Configure Gemini

Create `.env`:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

### Run the application

```bash
uv run streamlit run app.py
```

Then open the local Streamlit URL in your browser.

## 6. Observations and Result

For a ticket such as:

```text
Our API is returning 503 errors and customers cannot log in.
```

The system can:

- Classify it as **Technical**
- Assign higher urgency
- Identify potential need for human review
- Retrieve `technical.md`
- Generate a knowledge-grounded Gemini response

The main benefit is the separation of responsibilities:

```text
Laya   → What should happen?
RAG    → What evidence do we have?
Gemini → How should we communicate it?
```

## 7. Evaluation

The system can be evaluated using:

- **Laya:** department and urgency accuracy
- **RAG:** Top-K retrieval accuracy and relevance
- **Gemini:** relevance, factual grounding, and hallucination rate
- **End-to-End:** correctness of the final support workflow

A labeled test dataset can be used to measure these metrics.

## 8. Future Plan and Improvements

- Add PDF/DOCX knowledge sources
- Improve RAG with reranking and metadata filtering
- Add human-in-the-loop approval
- Store tickets and feedback in a database
- Add authentication and role-based access
- Add monitoring and automated evaluation
- Deploy the application for production use
