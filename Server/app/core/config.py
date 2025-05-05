from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Project metadata
    PROJECT_NAME: str = "SoulSpice"
    PROJECT_DESCRIPTION: str = "API pentru chatbot-ul SoulSpice - psiholog culinar"
    VERSION: str = "0.1.0"
    
    # API settings
    API_PREFIX: str = "/api"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # LM Studio settings (to be configured later)
    LM_STUDIO_API_URL: str = "http://localhost:1234/v1"
    LM_STUDIO_API_KEY: str = ""
    
    # Vector database settings (for FAISS/RAG)
    VECTOR_DB_PATH: str = "./data/vector_db"
    
    # Knowledge base settings
    KNOWLEDGE_BASE_PATH: str = "./data/knowledge"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()