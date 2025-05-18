from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.message import Message as DBMessage
from app.models.user import User

from app.models.message import MessageRequest, MessageResponse
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()
chat_service = ChatService(llm_service=llm_service)

@router.post("/process-message", response_model=MessageResponse)
async def process_message(
    message: MessageRequest,
    db: Session = Depends(get_db)
):
    """
    Process a user message and generate a response.
    This endpoint will be enhanced with LLM Studio integration.
    """
    if not message.text:
        raise HTTPException(status_code=400, detail="Mesajul nu poate fi gol")
    
    user = db.query(User).filter(User.id == message.sender).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Process the message using the chat service
    response_text = await chat_service.generate_response(message.text)

    user_msg = DBMessage(role="user", content=message.text, owner=user)
    assistant_msg = DBMessage(role="assistant", content=response_text, owner=user)
    
    db.add_all([user_msg, assistant_msg])
    db.commit()

    return MessageResponse(
        text=response_text,
        timestamp=datetime.now().isoformat()
    )

from app.models.message import ChatHistory

@router.get("/chat-history/{user_id}", response_model=ChatHistory)
def get_chat_history(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    messages = db.query(DBMessage).filter(DBMessage.user_id == user_id).order_by(DBMessage.id).all()
    return ChatHistory(
        messages=[
            {
                "role": m.role,
                "content": m.content,
                "timestamp": m.timestamp.isoformat() if m.timestamp else None
            } for m in messages
        ]
    )