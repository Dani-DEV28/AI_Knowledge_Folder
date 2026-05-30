from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse
from services.retrieval_service import retrieve_chunks
from services.ai_service import generate_answer

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
def chat(body: ChatRequest):
    """
    Accept a question with conversation history, retrieve relevant source chunks,
    and return a grounded answer with citations.
    """
    try:
        chunks = retrieve_chunks(body.assistant_id, body.question)
        response = generate_answer(body.question, chunks, body.history)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
