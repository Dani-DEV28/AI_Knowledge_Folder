from fastapi import APIRouter, UploadFile, File, Form
from models.schemas import AddWebsiteRequest, AddWebsiteResponse
from services.apify_service import trigger_crawl
from services.box_service import upload_file_to_box
from db.metadata import save_source, get_sources

router = APIRouter(prefix="/sources", tags=["Sources"])


@router.post("/website", response_model=AddWebsiteResponse)
async def add_website(body: AddWebsiteRequest):
    """
    Accept a website URL, trigger an Apify crawl, and store the result in Box.
    """
    result = await trigger_crawl(body.url, body.assistant_id)
    return result


@router.post("/upload")
async def upload_document(
    assistant_id: str = Form(...),
    file: UploadFile = File(...),
):
    """
    Upload a document (PDF, DOCX, TXT, JSON) and store it in Box.
    Supported types: .pdf, .docx, .txt, .json
    """
    content = await file.read()
    box_file_id = upload_file_to_box(file.filename, content, assistant_id)
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
    }


@router.get("")
def list_sources(assistant_id: str):
    """
    Return all knowledge sources associated with an assistant.
    """
    return get_sources(assistant_id)
