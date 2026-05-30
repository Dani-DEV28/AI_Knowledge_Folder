import boto3
import json
import os
from models.schemas import ChatResponse, SourceChunk

SYSTEM_PROMPT = """You are a trusted AI assistant.
Answer ONLY using the provided source excerpts below.
If the answer is not found in the excerpts, respond with exactly:
"I could not find information related to that question in the selected knowledge folder."
Always include source citations at the end of your answer.
Do not provide legal advice.
Do not use any outside knowledge."""

NOT_FOUND_RESPONSE = (
    "I could not find information related to that question in the selected knowledge folder."
)


def generate_answer(question: str, chunks: list) -> ChatResponse:
    """
    Build a grounded prompt from retrieved chunks and call AWS Bedrock.
    Falls back to NOT_FOUND_RESPONSE if no chunks are available.
    """
    if not chunks:
        return ChatResponse(answer=NOT_FOUND_RESPONSE, sources=[])

    context = "\n\n".join(
        f"[Source: {c['source_title']}]\n{c['text']}" for c in chunks
    )

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Sources:\n{context}\n\n"
        f"Question: {question}\n"
        f"Answer:"
    )

    answer_text = _call_bedrock(prompt)

    sources = [
        SourceChunk(
            text=c["text"][:300],
            source_title=c["source_title"],
            source_url=c.get("source_url", ""),
        )
        for c in chunks
    ]

    return ChatResponse(answer=answer_text, sources=sources)


def _call_bedrock(prompt: str) -> str:
    """
    Call AWS Bedrock (Claude Instant). Returns the model's completion text.
    If Bedrock is unavailable, raises an exception — swap in another LLM here as fallback.
    """
    region = os.getenv("BEDROCK_REGION", "us-east-1")
    client = boto3.client("bedrock-runtime", region_name=region)

    body = json.dumps(
        {
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "max_tokens_to_sample": 512,
            "temperature": 0.0,
            "stop_sequences": ["\n\nHuman:"],
        }
    )

    response = client.invoke_model(
        modelId="anthropic.claude-instant-v1",
        body=body,
        contentType="application/json",
        accept="application/json",
    )

    result = json.loads(response["body"].read())
    return result.get("completion", NOT_FOUND_RESPONSE).strip()
