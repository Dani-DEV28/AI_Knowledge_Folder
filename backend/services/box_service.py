import io
import os

from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth


def _get_client() -> BoxClient:
    """
    Build a Box client using a developer token from environment variables.
    For production, replace with OAuth2 or JWT auth.
    """
    token = os.getenv("BOX_ACCESS_TOKEN", "")
    auth = BoxDeveloperTokenAuth(token=token)
    return BoxClient(auth=auth)


def upload_file_to_box(filename: str, content: bytes, folder_name: str) -> str:
    """
    Upload a file to the Box folder matching folder_name (creates it if missing).
    Returns the Box file ID.
    """
    client = _get_client()
    folder_id = _get_or_create_folder(client, folder_name)
    file_stream = io.BytesIO(content)
    uploaded = client.uploads.upload_file(
        attributes={"name": filename, "parent": {"id": folder_id}},
        file=file_stream,
    )
    return uploaded.entries[0].id


def download_all_text_from_box(folder_name: str) -> list:
    """
    Download all .txt files from a Box folder.
    Returns a list of dicts: [{"filename": ..., "text": ...}]
    """
    client = _get_client()
    folder_id = _get_or_create_folder(client, folder_name)
    items = client.folders.get_folder_items(folder_id)

    results = []
    for item in items.entries:
        if item.name.endswith(".txt"):
            try:
                file_content = client.downloads.download_file(item.id)
                text = file_content.read().decode("utf-8", errors="ignore")
                results.append({"filename": item.name, "text": text})
            except Exception:
                continue
    return results


def _get_or_create_folder(client: BoxClient, folder_name: str) -> str:
    """
    Look for an existing top-level Box folder by name.
    Creates it if it does not exist.
    Returns the folder ID.
    """
    items = client.folders.get_folder_items("0")
    for item in items.entries:
        if item.name == folder_name:
            return item.id

    folder = client.folders.create_folder(name=folder_name, parent={"id": "0"})
    return folder.id
