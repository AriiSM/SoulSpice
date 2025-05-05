from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime

from app.models.message import MessageRequest, MessageResponse
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService

router = APIRouter()

@router.post("/process-message", response_model=MessageResponse)
async def process_message(
    message: MessageRequest,
    chat_service: ChatService = Depends(),
    llm_service: LLMService = Depends()
):
    """
    Process a user message and generate a response.
    This endpoint will be enhanced with LLM Studio integration.
    """
    if not message.text:
        raise HTTPException(status_code=400, detail="Mesajul nu poate fi gol")
    
    # Process the message using the chat service
    response_text = await chat_service.generate_response(message.text, llm_service)
    
    # Return the formatted response
    return MessageResponse(
        text=response_text,
        timestamp=datetime.now().isoformat()
    )