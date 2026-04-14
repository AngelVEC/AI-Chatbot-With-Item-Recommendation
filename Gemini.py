import google.genai as genai
import json

class GeminiService:
    def __init__(self, api_key: str, model: str = "gemini-3-flash-preview"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def extract_intent(self, user_query: str):
        prompt = f"""
        You are an intent parser for a product search system.

        Extract structured data from the user query.

        RULES:
        - Only return valid JSON
        - Do NOT include explanation
        - Keywords must be SHORT (1–2 words each)
        - Remove filler words like "I want", "recommend", etc.

        PRICE RULES:
        - "cheap", "budget", "affordable" → max_price = 800
        - "mid-range" → max_price = 1500
        - "expensive", "premium", "high-end" → max_price = null

        CATEGORY RULES:
        - laptop → "laptop"
        - pc, computer, desktop → "desktop"
        - gpu, graphics → "pc_component"
        - clothes, shirt, shoes → "clothing"

        Return JSON format:
        {{
        "keywords": ["...],
        "category": "from Category rules" or null,
        "max_price": "number from price rules" or null
        }}

        User query:
        "{user_query}"
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        try:
            return json.loads(response.text)
        except: 
            return {
                "keywords": user_query.split(),  # Fallback to using the whole query as keywords
                "category": None,
                "max_price": None
            }

    def recommend(self, query, products):
        product_text = "\n".join([
            f"{p['name']} - {p['description']} - {p['category']} - ${p['price']}" 
            for p in products
        ])

        prompt = f"""
        user query: "{query}"

        Here are some matching products based on the user's query:
        {product_text}

        Recommend the best options to the user based on their query and the product information above.
        """

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text



    def generate_response(self, prompt: str):
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text
