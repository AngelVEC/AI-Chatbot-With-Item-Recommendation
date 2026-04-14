class Chatbot:
    def __init__(self, gemini_service, database):
        self.gemini_service = gemini_service
        self.database = database
        self.memory = []
    
    #method to handle the query from the user, extract the intent, search for products, and generate a response
    def handle_query(self, user_query):
        intent = self.gemini_service.extract_intent(user_query)

        results = self.database.search_products(intent)

        if not results:
            fallback_intent = intent.copy()
            fallback_intent["keywords"] = []
            results = self.database.search_products(fallback_intent)

        if results:
            response = self.gemini_service.recommend(user_query, results, memory=self.memory)
        else:
            response = self.gemini_service.generate_response("No products found. Help the user to choose based on the recent conversation", memory=self.memory)
        
        #storing the memory of the conversation
        self.memory.append({"user": user_query, "bot": response})
        self.memory = self.memory[-5:]  # Keep only the last 5 conversations in memory

        return response