import os
from dotenv import load_dotenv
from Gemini import GeminiService
from Database import DatabaseManager
from Chatbot import Chatbot

#loading environment variables that saved on .env file
load_dotenv()

#Gemini Part
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

#initilaize the GeminiService with the API key
gemini = GeminiService(api_key=GEMINI_API_KEY)

#Initializing the database
db = DatabaseManager("products.db")

#initializing the chatbot with gemini and the database
bot = Chatbot(gemini, db)

#start the chat loop
while True:
    query = input("Please write your message (type 'exit' or 'quit' to close the chat): ")
    if query.lower() in ['exit', 'quit']:
        print("Goodbye!")
        break

    response = bot.handle_query(query)
    print("Bot:", response + "\n")


# #testing the generate_response method
# while True:
#     prompt = input("Please write your message (type 'exit' or 'quit' to close the chat): ")
#     if prompt.lower() in ['exit', 'quit']:
#         print("Goodbye!")
#         break

#     #print the user's message
#     print("You:", prompt + "\n")

#     #generate the response
#     response = gemini.generate_response(prompt)

#     #print the response
#     print("Bot:", response + "\n")

#Database Part

# #initialize the database
# db = DatabaseManager()
# #will ignore this even if the table already exists, so it's safe to call it every time
# db.create_table()

# #adding the product from the products.txt file to the database
# #db.add_products_from_text_file("products.txt")

# #check if product added
# all_products = db.get_all_products()
# print(f"Total products in database: {len(all_products)}")
# for product in all_products:
#     print(dict(product))  # Print each product as a dictionary