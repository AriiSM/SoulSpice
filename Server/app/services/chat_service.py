class ChatService:
    def __init__(self, llm_service):
        self.llm_service = llm_service

    async def generate_response(self, new_message: str, history: list) -> str:
        """
        Generate a response using LLM, with history as context.
        """
        if self.llm_service.is_available():
            try:
                full_prompt = self.build_prompt(history, new_message)
                return await self.llm_service.generate_response(full_prompt)
            except Exception as e:
                print(f"LLM service error: {e}")
                return "LLM service error: {e}"

    def build_prompt(self, history: list, new_message: str) -> str:
        prompt = ""
        for msg in history:
            role = msg.role or "user"
            prompt += f"{role}: {msg.content.strip()}\n"
        prompt += f"user: {new_message.strip()}\nassistant:"
        return prompt