from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.database import get_db
from app.models.user import User

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == request.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = pwd_context.hash(request.password)
    user = User(username=request.username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created", "user_id": user.id}

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": user.id}
