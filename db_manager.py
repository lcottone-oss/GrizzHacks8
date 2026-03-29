"""
Database manager for MongoDB Atlas connection and operations.
Handles fetching legal content, forms, and saving conversation history.
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

class DatabaseManager:
    def __init__(self):
        """Initialize MongoDB connection using MONGO_URI from .env"""
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client["hackathonDB"]
        self.legal_knowledge = self.db["legal_knowledge"]
        self.user_interactions = self.db["user_interactions"]
    
    def get_page_content(self, category, subtopic=None):
        """
        Fetch legal information, form links, and plain English summaries from MongoDB.
        
        Args:
            category (str): Main category (e.g., 'renters_rights', 'small_claims')
            subtopic (str, optional): Specific subtopic
        
        Returns:
            dict: Content including legal_info, forms, quick_facts, and plain_english
        """
        try:
            if subtopic:
                # Fetch specific subtopic content
                result = self.legal_knowledge.find_one({
                    "category": category,
                    "subtopics.name": subtopic
                })
                if result:
                    for sub in result["subtopics"]:
                        if sub["name"] == subtopic:
                            return sub
            else:
                # Fetch full category content
                result = self.legal_knowledge.find_one({"category": category})
                if result:
                    return result
            
            return None
        except Exception as e:
            print(f"Error fetching content: {str(e)}")
            return None
    
    def get_forms_and_links(self, category):
        """
        Fetch forms and resource links for a category from laws.json structure.
        
        Args:
            category (str): Main category
        
        Returns:
            dict: Forms and links
        """
        try:
            import json
            with open("laws.json", "r") as file:
                laws_data = json.load(file)
            return laws_data.get(category, {})
        except Exception as e:
            print(f"Error fetching forms: {str(e)}")
            return {}
    
    def save_conversation_history(self, category, subtopic, messages, user_state=None):
        """
        Save chatbot conversation history anonymously for tracking common issues.
        
        Args:
            category (str): Main topic category
            subtopic (str): Subtopic area
            messages (list): List of message dicts with role and content
            user_state (str, optional): User's situation summary
        
        Returns:
            str: ID of saved interaction
        """
        try:
            interaction = {
                "timestamp": datetime.utcnow(),
                "category": category,
                "subtopic": subtopic,
                "messages": messages,
                "user_state": user_state,
                "message_count": len(messages)
            }
            result = self.user_interactions.insert_one(interaction)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error saving conversation: {str(e)}")
            return None
    
    def get_category_summary(self, category):
        """
        Get a category with all its subtopics and quick facts.
        
        Args:
            category (str): Main category
        
        Returns:
            dict: Full category data
        """
        try:
            result = self.legal_knowledge.find_one({"category": category})
            return result
        except Exception as e:
            print(f"Error getting category summary: {str(e)}")
            return None

# Global instance
db_manager = DatabaseManager()
