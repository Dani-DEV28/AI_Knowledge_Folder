from fastapi import APIRouter
from models.schemas import CreateAssistantRequest, CreateAssistantResponse
from db.metadata import save_assistant

router = APIRouter(prefix="/assistants", tags=["Assistants"])


@router.post("", response_model=CreateAssistantResponse)
def create_assistant(body: CreateAssistantRequest):
    """
    Create a new AI assistant backed by a Box folder.
    """
    assistant = save_assistant(body.name, body.description, body.folder_name)
    return CreateAssistantResponse(
        assistant_id=assistant["id"],
        name=assistant["name"],
        folder_name=assistant["folder_name"],
    )
