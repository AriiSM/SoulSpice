from app.services.llm_service import LLMService

class ChatService:
    def __init__(
        self,
        llm_service,
    ):
        self.llm_service = llm_service
        
    async def generate_response(self, message: str) -> str:
        """
        Generate a response based on the user's message.
        This method will be enhanced with LLM integration.
        """
        if self.llm_service.is_available():
            try:
                return await self.llm_service.generate_response(message)
            except Exception as e:
                print(f"LLM service error: {e}")
    
