import re
import json
from .models import Intent

class IntentRecognizer:
    def __init__(self):
        # Load intents from database
        self.intents = {intent.name: intent.keywords for intent in Intent.objects.all()}
    
    def recognize_intent(self, message):
        message = message.lower()
        
        # Add direct checks for common ordering phrases
        order_phrases = ["order", "like to order", "want to order", "get", "buy", "purchase"]
        for phrase in order_phrases:
            if phrase in message:
                return "place_order"
        
        # Continue with existing keyword matching
        for intent_name, keywords in self.intents.items():
            for keyword in keywords:
                if keyword.lower() in message:
                    return intent_name
        
        # If no intent matches, return a default intent
        return "unknown"
    
    def extract_order_details(self, message, intent):
        """Extract order details based on recognized intent"""
        if intent == "place_order":
            # Simple regex pattern to extract order details
            # In a real system, you'd want more sophisticated NLP here
            products = re.findall(r'(\d+)\s+([a-zA-Z\s]+)', message)
            order_items = [{"quantity": int(qty), "product": product.strip()} 
                           for qty, product in products]
            return {"items": order_items}
        
        return {}