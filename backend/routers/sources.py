from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from models.schemas import AddWebsiteRequest, AddWebsiteResponse
from services.apify_service import trigger_crawl, ingest_run_results
from services.box_service import upload_file_to_box
from services.document_service import extract_text, save_uploaded_text
from db.metadata import save_source, get_sources, get_assistant

router = APIRouter(prefix="/sources", tags=["Sources"])


@router.post("/website", response_model=AddWebsiteResponse)
async def add_website(body: AddWebsiteRequest):
    """
    Accept a website URL, trigger an Apify crawl, wait for it to finish,
    then automatically ingest the results into the knowledge base.
    """
    try:
        result = await trigger_crawl(body.url, body.assistant_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/website/ingest/{run_id}")
async def ingest_website(run_id: str, assistant_id: str):
    """
    Fetch completed Apify run results and ingest them into the knowledge base.
    Call this after POST /sources/website once the crawl has finished (~1-2 min).
    Returns pages_ingested count and status.
    """
    try:
        result = await ingest_run_results(run_id, assistant_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_document(
    assistant_id: str = Form(...),
    file: UploadFile = File(...),
):
    """
    Upload a document (PDF, TXT, JSON), extract its text,
    upload extracted text to Box, and store the original in Box too.
    Everything lives in Box — no local storage.
    """
    content = await file.read()

    # Resolve Box folder name from assistant record (use name, not UUID)
    assistant = get_assistant(assistant_id)
    folder_name = assistant["folder_name"] if assistant else assistant_id

    # Extract text from the document
    text = ""
    text_error = None
    try:
        text = extract_text(file.filename, content)
    except Exception as e:
        text_error = str(e)

    # Upload original file to Box
    box_file_id = None
    try:
        box_file_id = upload_file_to_box(file.filename, content, folder_name)
    except Exception:
        pass

    # Upload extracted text as .txt to Box (this is what retrieval searches)
    text_box_id = None
    if text:
        txt_filename = file.filename.rsplit(".", 1)[0] + "_extracted.txt"
        try:
            text_box_id = upload_file_to_box(txt_filename, text.encode("utf-8"), folder_name)
        except Exception:
            pass

    save_source(
        assistant_id=assistant_id,
        file_name=file.filename,
        source_type="upload",
        source_url=None,
        box_file_id=box_file_id,
    )

    return {
        "status": "uploaded",
        "file_name": file.filename,
        "box_file_id": box_file_id,
        "text_extracted": bool(text),
        "characters_extracted": len(text),
        "text_box_id": text_box_id,
        "extraction_error": text_error,
    }


@router.get("")
def list_sources(assistant_id: str):
    """
    Return all knowledge sources associated with an assistant.
    """
    return get_sources(assistant_id)


@router.delete("/{source_id}")
def delete_source(source_id: str, assistant_id: str):
    """
    Delete a source from metadata and from Box.
    """
    from db.metadata import delete_source_by_id, get_source_by_id
    from services.box_service import delete_file_from_box

    source = get_source_by_id(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    # Delete from Box if it has a box_file_id
    if source.get("box_file_id"):
        try:
            delete_file_from_box(source["box_file_id"])
        except Exception:
            pass  # Box deletion failure shouldn't block

    # Delete from metadata
    delete_source_by_id(source_id)

    return {"status": "deleted", "source_id": source_id}
