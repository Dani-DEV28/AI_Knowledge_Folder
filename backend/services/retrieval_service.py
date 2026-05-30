from pathlib import Path

SEED_DIR = Path(__file__).parent.parent / "seed"
CHUNK_SIZE = 500  # words per chunk


def retrieve_chunks(assistant_id: str, question: str, top_k: int = 5) -> list:
    """
    MVP keyword retrieval.
    Loads all .txt files from the seed directory, splits them into chunks,
    scores each chunk against the question words, and returns the top results.

    Replace with embedding-based search if time allows after core MVP is working.
    """
    question_words = set(question.lower().split())
    results = []

    if not SEED_DIR.exists():
        return []

    for file in SEED_DIR.glob("*.txt"):
        text = file.read_text(encoding="utf-8")
        chunks = _split_chunks(text, CHUNK_SIZE)
        for chunk in chunks:
            score = _score(chunk, question_words)
            if score > 0:
                results.append(
                    {
                        "text": chunk,
                        "source_title": file.stem.replace("_", " ").title(),
                        "source_url": "",
                        "score": score,
                    }
                )

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def _split_chunks(text: str, chunk_size: int) -> list:
    words = text.split()
    return [
        " ".join(words[i : i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]


def _score(chunk: str, question_words: set) -> int:
    chunk_words = set(chunk.lower().split())
    return len(question_words & chunk_words)
