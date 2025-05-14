from app.services.chat_bot_tools import SemanticSearchAssistant
from app.services.chat_bot_tools import TextChunkLoader, SemanticRetriever, ToxicityFilter, ResponseGenerator

from app.core.config import settings

class LLMService:
    def __init__(self):
        self.api_url = settings.LM_STUDIO_API_KEY
        self.api_key = settings.LM_STUDIO_API_KEY
        self._is_available = True
        
        ## Initialize the chatbot with the SemanticSearchAssistant
        self.loader = TextChunkLoader()
        self.recipes = self.loader.load_chunks(settings.RECIPES_DATASET_PATH)
        self.convs = self.loader.load_chunks(settings.CONVERSATIONS_DATASET_PATH)

        self.retriever = SemanticRetriever(settings.SEMANTIC_SEARCH_MODEL, settings.RECIPES_FAISS_PATH, settings.CONVERSATIONS_FAISS_PATH, self.recipes, self.convs)
        self.toxic = ToxicityFilter()
        self.responder = ResponseGenerator(settings.LM_STUDIO_API_URL, settings.LM_STUDIO_API_KEY, settings.LM_STUDIO_MODEL_NAME)

        self.assistant = SemanticSearchAssistant(self.retriever, self.responder, self.toxic)
        
    def is_available(self) -> bool:
        """Check if the LLM service is available and configured."""
        # This will be implemented to check if LM Studio is running
        return self._is_available and bool(self.api_key)
    
    async def generate_response(self, message: str) -> str:
        """
        Generate a response using LM Studio.
        This is a placeholder for future implementation.
        """
        if not self.is_available():
            raise ValueError("LLM service is not available")
        
        return await self.assistant.ask(message)