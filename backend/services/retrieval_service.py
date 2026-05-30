from pathlib import Path
from services.box_service import download_all_text_from_box
from db.metadata import get_assistant

SEED_DIR = Path(__file__).parent.parent / "seed"
CHUNK_SIZE = 500  # words per chunk


def retrieve_chunks(assistant_id: str, question: str, top_k: int = 5) -> list:
    """
    Keyword retrieval from two sources:
    1. seed/         — pre-loaded RCW text files (always available, local fallback)
    2. Box folder    — all .txt files in the assistant's Box folder (source of truth)

    Scores each chunk by word overlap with the question.
    Returns top_k results sorted by score.
    """
    question_words = set(question.lower().split())
    results = []

    # 1. Seed files (local fallback, always available)
    if SEED_DIR.exists():
        for file in SEED_DIR.glob("*.txt"):
            _score_file_local(file, question_words, results)

    # 2. Box folder (source of truth for uploaded + crawled content)
    try:
        assistant = get_assistant(assistant_id)
        folder_name = assistant["folder_name"] if assistant else assistant_id
        box_files = download_all_text_from_box(folder_name)
        for bf in box_files:
            _score_text(bf["filename"], bf["text"], question_words, results)
    except Exception:
        pass  # Box unavailable — fall back to seed only

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
