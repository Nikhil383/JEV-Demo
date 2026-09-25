from google import genai

from src.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_response(
    customer_message: str,
    decision: dict,
    documents: list,
):

    evidence = "\n\n".join(
        f"Source: {metadata['source']}\n{document}"
        for document, metadata in documents
    )

    prompt = f"""
You are a customer-support response assistant.

Customer message:
{customer_message}

Routing decision:
Department: {decision['department']}
Urgency: {decision['urgency']}

Verified knowledge-base evidence:
{evidence}

Rules:

1. Answer using the provided evidence.
2. Do not invent company policies.
3. Do not claim that an action such as a refund
   was completed unless the evidence explicitly
   confirms it.
4. If the evidence is insufficient, say so.
5. Keep the response concise and helpful.
6. Do not mention internal model names or routing logic.

Write the response that should be shown to the customer.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    return response.text