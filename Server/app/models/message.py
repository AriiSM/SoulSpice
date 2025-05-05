from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class MessageRequest(BaseModel):
    text: str
    sender: str
    timestamp: Optional[str] = None

class MessageResponse(BaseModel):
    text: str
    timestamp: str

class ChatHistory(BaseModel):
    messages: List[Dict[str, Any]] = []