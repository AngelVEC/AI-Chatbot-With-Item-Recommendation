import os
from dotenv import load_dotenv
from Gemini import GeminiService

#loading environment variables that saved on .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

#initilaize the GeminiService with the API key
gemini = GeminiService(api_key=GEMINI_API_KEY)

#testing the generate_response method
prompt = "recommend me a cheap laptop for programming"
response = gemini.generate_response(prompt)
print(response)