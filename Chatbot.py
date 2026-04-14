class Chatbot:
    def __init__(self, gemini_service, database):
        self.gemini_service = gemini_service
        self.database = database
    
    def handle_query(self, user_query):
        intent = self.gemini_service.extract_intent(user_query)

        results = self.database.search_products(intent)

        if not results:
            fallback_intent = intent.copy()
            fallback_intent["keywords"] = []
            results = self.database.search_products(fallback_intent)

        if results:
            return self.gemini_service.recommend(user_query, results)

        return "I couldn't find any products matching your query. try different keywords or check back later when we have more products in our database!"