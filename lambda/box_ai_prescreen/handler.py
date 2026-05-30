"""
Lambda: Box AI Pre-Screen → Bedrock Final Answer

Flow:
1. Receives a question + Box folder ID
2. Uses Box AI to search/extract relevant document passages (pre-screen)
3. Passes pre-screened content to Bedrock Claude for final grounded answer
4. Returns answer with source citations
"""

import json
import os
import boto3
from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth, BoxJWTAuth
from box_sdk_gen.managers.ai import CreateAiAskMode, CreateAiAskItems


def get_box_client() -> BoxClient:
    """Build Box client from JWT config or developer token."""
    jwt_config = os.environ.get("BOX_JWT_CONFIG")
    if jwt_config:
        config = json.loads(jwt_config)
        auth = BoxJWTAuth.from_settings_dictionary(config)
        return BoxClient(auth=auth)
    token = os.environ.get("BOX_ACCESS_TOKEN", "")
    auth = BoxDeveloperTokenAuth(token=token)
    return BoxClient(auth=auth)


def box_ai_prescreen(client: BoxClient, question: str, folder_id: str) -> list:
    """
    Stage 1: Use Box AI to extract relevant passages from folder documents.
    Returns list of dicts with text excerpts and source metadata.
    """
    # Search for relevant files in the folder
    search_results = client.search.search_for_content(
        query=question,
        ancestor_folder_ids=[folder_id],
        content_types=["name", "description", "file_content"],
        limit=5,
    )

    if not search_results.entries:
        return []

    # Use Box AI ask to extract relevant passages from found files
    items = [
        CreateAiAskItems(id=item.id, type="file")
        for item in search_results.entries[:5]
    ]

    try:
        ai_response = client.ai.create_ai_ask(
            mode=CreateAiAskMode.MULTIPLE_ITEM_QA,
            prompt=f"Extract the sections most relevant to this question: {question}",
            items=items,
        )
        return [{
            "text": ai_response.answer,
            "source_title": ", ".join(item.name for item in search_results.entries[:5]),
            "source_url": "",
            "file_ids": [item.id for item in search_results.entries[:5]],
        }]
    except Exception:
        # Fallback: return raw search result names as context
        results = []
        for item in search_results.entries[:5]:
            try:
                content = client.downloads.download_file(item.id)
                text = content.read().decode("utf-8", errors="ignore")[:2000]
                results.append({
                    "text": text,
                    "source_title": item.name,
                    "source_url": "",
                })
            except Exception:
                continue
        return results


def bedrock_final_answer(question: str, prescreened_chunks: list, history: list = None) -> str:
    """
    Stage 2: Send pre-screened content to Bedrock Claude for final answer.
    """
    if not prescreened_chunks:
        return "I could not find information related to that question in the selected knowledge folder."

    context = "\n\n---\n\n".join(
        f"[Source: {c['source_title']}]\n{c['text']}" for c in prescreened_chunks
    )

    system_prompt = (
        "You are a trusted AI assistant. "
        "Answer ONLY using the provided source excerpts below. "
        "If the answer is not found in the excerpts, say so. "
        "Always cite which source your answer comes from. "
        "Do not provide legal advice. Do not use outside knowledge."
    )

    region = os.environ.get("BEDROCK_REGION", "us-east-1")
    model_id = os.environ.get("BEDROCK_MODEL_ID", "us.anthropic.claude-haiku-4-5-20251001-v1:0")
    client = boto3.client("bedrock-runtime", region_name=region)

    messages = []
    if history:
        for msg in history[-10:]:
            if msg.get("role") in ("user", "assistant") and msg.get("content"):
                messages.append({"role": msg["role"], "content": [{"text": msg["content"]}]})

    messages.append({
        "role": "user",
        "content": [{"text": f"Sources:\n{context}\n\nQuestion: {question}"}],
    })

    response = client.converse(
        modelId=model_id,
        system=[{"text": system_prompt}],
        messages=messages,
        inferenceConfig={"maxTokens": 512, "temperature": 0.0},
    )

    return response["output"]["message"]["content"][0]["text"].strip()


def handler(event, context):
    """
    Lambda entry point.

    Expected event:
    {
        "question": "What does the law say about...",
        "folder_id": "123456789",
        "history": [{"role": "user", "content": "..."}]  // optional
    }
    """
    body = json.loads(event.get("body", "{}")) if isinstance(event.get("body"), str) else event
    question = body.get("question", "")
    folder_id = body.get("folder_id", os.environ.get("BOX_FOLDER_ID", "0"))
    history = body.get("history", [])

    if not question:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "question is required"}),
        }

    # Stage 1: Box AI pre-screens documents
    box_client = get_box_client()
    prescreened = box_ai_prescreen(box_client, question, folder_id)

    # Stage 2: Bedrock generates final grounded answer
    answer = bedrock_final_answer(question, prescreened, history)

    sources = [
        {"source_title": c["source_title"], "text": c["text"][:300], "source_url": c.get("source_url", "")}
        for c in prescreened
    ]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"answer": answer, "sources": sources}),
    }
