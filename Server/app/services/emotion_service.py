from typing import List

class EmotionService:
    def identify_emotion_or_food_preference(self, text: str) -> List[str]:
        """
        Identify emotions or food preferences from text.
        This will be enhanced with ML-based emotion detection in the future.
        """
        text = text.lower()
        
        emotions = []
        
        # Identify emotions from text
        if any(word in text for word in ["fericit", "bucurie", "bucuros", "vesel", "bine"]):
            emotions.append("fericit")
        
        if any(word in text for word in ["trist", "supărat", "deprimat", "depresie", "melancolie"]):
            emotions.append("trist")
        
        if any(word in text for word in ["stresat", "anxios", "anxietate", "stres", "nervos", "tensionat"]):
            emotions.append("stresat")
        
        if any(word in text for word in ["obosit", "epuizat", "lipsit de energie", "fără putere"]):
            emotions.append("obosit")
        
        # Identify food preferences
        if any(word in text for word in ["dulce", "ciocolată", "desert", "prăjitură", "zahăr"]):
            emotions.append("poftă_dulce")
        
        if any(word in text for word in ["sărat", "chips", "crocant", "sărate"]):
            emotions.append("poftă_sărat")
        
        return emotions if emotions else ["general"]