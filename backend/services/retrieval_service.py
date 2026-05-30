import os
from pathlib import Path
from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth
from box_sdk_gen.managers.ai import CreateAiAskMode, AiItemAsk
from services.box_service import download_all_text_from_box
from db.metadata import get_assistant

SEED_DIR = Path(__file__).parent.parent / "seed"
CHUNK_SIZE = 500  # words per chunk


def retrieve_chunks(assistant_id: str, question: str, top_k: int = 5) -> list:
    """
    Two-stage retrieval:
    1. Try Box AI pre-screen (semantic search + AI passage extraction)
    2. Fall back to keyword search if Box AI is unavailable

    Box AI provides better results by understanding meaning, not just keywords.
    """
    # Stage 1: Try Box AI pre-screen
    try:
        assistant = get_assistant(assistant_id)
        folder_name = assistant["folder_name"] if assistant else assistant_id
        results = _box_ai_prescreen(question, folder_name)
        if results:
            return results[:top_k]
    except Exception:
        pass  # Box AI unavailable, fall through to keyword search

    # Stage 2: Keyword fallback
    return _keyword_search(assistant_id, question, top_k)


def _box_ai_prescreen(question: str, folder_name: str) -> list:
    """Use Box AI to search and extract relevant passages."""
    token = os.getenv("BOX_ACCESS_TOKEN", "")
    if not token:
        return []

    auth = BoxDeveloperTokenAuth(token=token)
    client = BoxClient(auth=auth)

    # Find the folder ID
    items = client.folders.get_folder_items("0")
    folder_id = None
    for item in items.entries:
        if item.name == folder_name:
            folder_id = item.id
            break
    if not folder_id:
        return []

    # Search for relevant files
    search_results = client.search.search_for_content(
        query=question,
        ancestor_folder_ids=[folder_id],
        content_types=["name", "description", "file_content"],
        limit=5,
    )

    if not search_results.entries:
        return []

    # Use Box AI to extract relevant passages
    ai_items = [
        AiItemAsk(id=item.id, type="file")
        for item in search_results.entries[:5]
    ]

    try:
        ai_response = client.ai.create_ai_ask(
            mode=CreateAiAskMode.MULTIPLE_ITEM_QA,
            prompt=f"Extract the sections most relevant to: {question}",
            items=ai_items,
        )
        return [{
            "text": ai_response.answer,
            "source_title": ", ".join(item.name for item in search_results.entries[:5]),
            "source_url": "",
            "score": 100,
        }]
    except Exception:
        # Box AI ask failed — return raw file content as fallback
        results = []
        for item in search_results.entries[:5]:
            try:
                content = client.downloads.download_file(item.id)
                text = content.read().decode("utf-8", errors="ignore")[:2000]
                results.append({
                    "text": text,
                    "source_title": item.name,
                    "source_url": "",
                    "score": 50,
                })
            except Exception:
                continue
        return results


def _keyword_search(assistant_id: str, question: str, top_k: int) -> list:
    """Original keyword-based retrieval as fallback."""
    question_words = set(question.lower().split())
    results = []

    if SEED_DIR.exists():
        for file in SEED_DIR.glob("*.txt"):
            _score_file_local(file, question_words, results)

    try:
        assistant = get_assistant(assistant_id)
        folder_name = assistant["folder_name"] if assistant else assistant_id
        box_files = download_all_text_from_box(folder_name)
        for bf in box_files:
            _score_text(bf["filename"], bf["text"], question_words, results)
    except Exception:
        pass

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def _score_file_local(file: Path, question_words: set, results: list) -> None:
    """Read a local file, split into chunks, score each."""
    try:
        text = file.read_text(encoding="utf-8")
    except Exception:
        return
    _score_text(file.stem, text, question_words, results)


def _score_text(source_name: str, text: str, question_words: set, results: list) -> None:
    """Split text into chunks and score each against question words."""
    # Extract source URL from first lines if present
    source_url = ""
    lines = text.splitlines()
    for line in lines[:3]:
        if line.startswith("Source:"):
            source_url = line.replace("Source:", "").strip()
            break

    chunks = _split_chunks(text, CHUNK_SIZE)
    for chunk in chunks:
        score = _score(chunk, question_words)
        if score > 0:
            results.append({
                "text": chunk,
                "source_title": source_name.replace("_", " ").title(),
                "source_url": source_url,
                "score": score,
            })


def _split_chunks(text: str, chunk_size: int) -> list:
    words = text.split()
    return [
        " ".join(words[i: i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]


def _score(chunk: str, question_words: set) -> int:
    chunk_words = set(chunk.lower().split())
    return len(question_words & chunk_words)
