from fastapi import Depends
from typing import List, Dict, Any, Optional
import random

from app.data.knowledge_base import FOOD_MOOD_KNOWLEDGE, RECIPES, GENERAL_RESPONSES
from app.services.emotion_service import EmotionService
from app.services.llm_service import LLMService
from app.services.vector_service import VectorService

class ChatService:
    def __init__(
        self,
        emotion_service: EmotionService = Depends(),
        vector_service: VectorService = Depends()
    ):
        self.emotion_service = emotion_service
        self.vector_service = vector_service
    
    async def generate_response(self, message: str, llm_service: LLMService) -> str:
        """
        Generate a response based on the user's message.
        This method will be enhanced with LLM integration.
        """
        # Check if LLM service is available and configured
        if llm_service.is_available():
            try:
                # This will be implemented when LLM Studio is integrated
                return await llm_service.generate_response(message)
            except Exception as e:
                print(f"LLM service error: {e}")
                # Fall back to rule-based response if LLM fails
        
        # Rule-based response generation (fallback)
        return await self._generate_rule_based_response(message)
    
    async def _generate_rule_based_response(self, message: str) -> str:
        """
        Generate a rule-based response using the knowledge base.
        This is a fallback method when LLM is not available.
        """
        # Identify emotions or food preferences
        categories = self.emotion_service.identify_emotion_or_food_preference(message)
        
        response_parts = []
        
        # Add a general response if no specific category is identified
        if "general" in categories:
            response_parts.append(random.choice(GENERAL_RESPONSES))
            response_parts.append("Poți să-mi spui cum te simți sau ce poftă ai, și îți pot oferi recomandări personalizate.")
            return " ".join(response_parts)
        
        # Add nutritional advice based on emotions/preferences
        for category in categories:
            if category in FOOD_MOOD_KNOWLEDGE:
                response_parts.append(random.choice(FOOD_MOOD_KNOWLEDGE[category]))
        
        # Add a recipe if available for the identified category
        recipe_categories = [cat for cat in categories if cat in RECIPES]
        if recipe_categories:
            category = random.choice(recipe_categories)
            recipe = random.choice(RECIPES[category])
            response_parts.append(f"\n\nIată o rețetă care ți-ar putea plăcea: **{recipe['nume']}**")
            response_parts.append("\nIngrediente:")
            response_parts.append(", ".join(recipe['ingrediente']))
            response_parts.append("\nPreparare:")
            response_parts.append(recipe['preparare'])
        
        # Add an invitation at the end
        response_parts.append("\n\nAi vreo întrebare specifică despre această recomandare sau despre cum te poate ajuta alimentația să-ți îmbunătățești starea?")
        
        return " ".join(response_parts)