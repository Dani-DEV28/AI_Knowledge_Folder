import json
import uuid
from pathlib import Path
from datetime import datetime, timezone

DB_FILE = Path(__file__).parent / "data.json"


def _load() -> dict:
    if not DB_FILE.exists():
        return {"assistants": [], "sources": []}
    return json.loads(DB_FILE.read_text(encoding="utf-8"))


def _save(data: dict) -> None:
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    DB_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def save_assistant(name: str, description: str, folder_name: str) -> dict:
    data = _load()
    assistant = {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": description,
        "folder_name": folder_name,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    data["assistants"].append(assistant)
    _save(data)
    return assistant


def get_assistant(assistant_id: str) -> dict | None:
    data = _load()
    for a in data["assistants"]:
        if a["id"] == assistant_id:
            return a
    return None


def save_source(
    assistant_id: str,
    file_name: str,
    source_type: str,
    source_url: str | None,
    box_file_id: str | None,
) -> dict:
    data = _load()
    source = {
        "id": str(uuid.uuid4()),
        "assistant_id": assistant_id,
        "file_name": file_name,
        "source_type": source_type,   # "website" or "upload"
        "source_url": source_url,
        "box_file_id": box_file_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }
    data["sources"].append(source)
    _save(data)
    return source


def get_sources(assistant_id: str) -> list:
    data = _load()
    return [s for s in data["sources"] if s["assistant_id"] == assistant_id]


def get_source_by_id(source_id: str) -> dict | None:
    data = _load()
    for s in data["sources"]:
        if s["id"] == source_id:
            return s
    return None


def delete_source_by_id(source_id: str) -> bool:
    data = _load()
    original_len = len(data["sources"])
    data["sources"] = [s for s in data["sources"] if s["id"] != source_id]
    if len(data["sources"]) < original_len:
        _save(data)
        return True
    return False
