from pydantic import BaseModel
from typing import Optional, List


class CreateAssistantRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    folder_name: str


class CreateAssistantResponse(BaseModel):
    assistant_id: str
    name: str
    folder_name: str


class AddWebsiteRequest(BaseModel):
    assistant_id: str
    url: str


class AddWebsiteResponse(BaseModel):
    status: str
    run_id: str
    url: str
    pages_ingested: Optional[int] = 0
    message: Optional[str] = None


class ChatRequest(BaseModel):
    assistant_id: str
    question: str


class SourceChunk(BaseModel):
    text: str
    source_title: str
    source_url: Optional[str] = ""


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
