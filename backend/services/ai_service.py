import os
import boto3
from botocore.exceptions import NoCredentialsError, EndpointResolutionError, ClientError
from models.schemas import ChatResponse, SourceChunk

NOT_FOUND_RESPONSE = (
    "I could not find information related to that question in the selected knowledge folder."
)

SYSTEM_PROMPT = """You are a trusted AI assistant.
Answer ONLY using the provided source excerpts below.
If the answer is not found in the excerpts, respond with exactly:
"I could not find information related to that question in the selected knowledge folder."
Always include source citations at the end of your answer.
Do not provide legal advice.
Do not use any outside knowledge."""


def generate_answer(question: str, chunks: list, history: list = None) -> ChatResponse:
    if history is None:
        history = []

    if not chunks:
        return ChatResponse(answer=NOT_FOUND_RESPONSE, sources=[])

    sources = [
        SourceChunk(
            text=c["text"][:300],
            source_title=c["source_title"],
            source_url=c.get("source_url", ""),
        )
        for c in chunks
    ]

    # Try Bedrock first, fall back to local summary if not configured
    try:
        answer_text = _call_bedrock(question, chunks, history)
    except (NoCredentialsError, EndpointResolutionError, ClientError, Exception):
        answer_text = _local_fallback(question, chunks)

    return ChatResponse(answer=answer_text, sources=sources)


def _call_bedrock(question: str, chunks: list, history: list) -> str:
    context = "\n\n".join(
        f"[Source: {c['source_title']}]\n{c['text']}" for c in chunks
    )

    region = os.getenv("BEDROCK_REGION", "us-east-1")
    model_id = os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-haiku-4-5-20251001-v1:0")
    client = boto3.client("bedrock-runtime", region_name=region)

    # Build messages with conversation history for follow-up context
    messages = []

    # Add previous conversation turns (last 10 messages max to stay within limits)
    for msg in history[-10:]:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role in ("user", "assistant") and content:
            messages.append({
                "role": role,
                "content": [{"text": content}]
            })

    # Add current question with sources
    messages.append({
        "role": "user",
        "content": [
            {"text": f"Sources:\n{context}\n\nQuestion: {question}"}
        ]
    })

    response = client.converse(
        modelId=model_id,
        system=[{"text": SYSTEM_PROMPT}],
        messages=messages,
        inferenceConfig={
            "maxTokens": 512,
            "temperature": 0.0,
        }
    )

    return response["output"]["message"]["content"][0]["text"].strip()


def _local_fallback(question: str, chunks: list) -> str:
    lines = [
        "Based on the available knowledge sources, here is what was found:\n"
    ]
    for c in chunks:
        lines.append(f"[{c['source_title']}]\n{c['text'][:400]}\n")

    lines.append(
        "\nNote: This response was generated without an AI model. "
        "Configure BEDROCK credentials in .env for full AI-generated answers."
    )
    return "\n".join(lines)
