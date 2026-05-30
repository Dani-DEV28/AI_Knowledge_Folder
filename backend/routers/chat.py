from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse
from services.retrieval_service import retrieve_chunks
from services.ai_service import generate_answer

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
def chat(body: ChatRequest):
    """
    Accept a question, retrieve relevant source chunks, and return a grounded AI answer with citations.
    """
    chunks = retrieve_chunks(body.assistant_id, body.question)
    response = generate_answer(body.question, chunks)
    return response
