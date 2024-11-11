import google.generativeai as genai

from transformers import pipeline
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# HERE YOU HAVE TO SET UP YOUR CONFIGURATIONS

BOT_TOKEN = 'your_token'

# MODEL CONFIGS

genai.configure(api_key=f"your_token")

model = genai.GenerativeModel(model_name = "gemini-1.5-flash-002", 
                              safety_settings = {HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE},
                              system_instruction="""You are very polite, your name is CookBook, 
                                                    you are young sheaf who is 23 years old. 
                                                    You are always glad to help any person with the recipe, 
                                                    according to what products the person has. 
                                                    You are always flexible and open for discussion of the recipes and adjusting them to user needs. 
                                                    Make sure to use no more than 300 words per answer!
                                                    Make sure to support conversation only about food and recipes! Not something different"""
                             )





# Initialize the translation pipeline
translator = pipeline("translation_en_to_ru", model="Helsinki-NLP/opus-mt-en-ru")