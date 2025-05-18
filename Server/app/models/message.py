from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class MessageRequest(BaseModel):
    text: str
    sender: int
    timestamp: Optional[str] = None

class MessageResponse(BaseModel):
    text: str
    timestamp: str

class ChatHistory(BaseModel):
    messages: List[Dict[str, Any]] = []

#DB

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="messages")