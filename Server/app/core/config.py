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
    LM_STUDIO_API_KEY: str = "no-key-needed"
    LM_STUDIO_MODEL_NAME: str = "mistral-7b-instruct-v0.3"
    
    # FAISS settings
    RECIPES_DATASET_PATH: str = "app/data/faiss/parsed_recipes.txt"
    CONVERSATIONS_DATASET_PATH: str = "app/data/faiss/parsed_conversations.txt"
    
    RECIPES_FAISS_PATH: str = "app/data/faiss/recipes.faiss"
    CONVERSATIONS_FAISS_PATH: str = "app/data/faiss/conversations.faiss"
    
    SEMANTIC_SEARCH_MODEL: str = "all-MiniLM-L6-v2"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()