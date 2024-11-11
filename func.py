# imports
import re
import json

import google.generativeai as genai

from typing import List
from typing_extensions import TypedDict
from tqdm.notebook import tqdm
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from translate import Translator
from config import model, translator


### CUSTOM FUNCTIONS ###


def get_gemini_greeting_response() -> str:
    prompt = (f"Hi!"
              "Make sure that your greeting response is not longer than 2 sentences")

    try:
        _response = model.generate_content(prompt)
        response = _response.candidates[0].content.parts[0].text
        role = _response.candidates[0].content.role

        return response, role

    except Exception as e:
        print(f"Error encountered: {e}")
        return f"Failure: {e}"

def get_first_recipes(user_input: str, context: List):
            
    user_input = f"""You do not have to greet me again!. 
                here is the list of the products that i have: 
                {user_input}. 
                Make sure your response is no longer than 300 words. 
                Give me list of 3 recipes that i can cook out of this. 
                Give 1 easy and fast recipe, give 1 middle difficulty recipe and 1 vegan recipe. 
                If it is impossible to create a vegan mean out of products you have, give 1 hard difficulty recipe."""
    
    chat = model.start_chat(
            history=context,
        )
    
    try:
        
        _response = chat.send_message(user_input)

        response = _response.candidates[0].content.parts[0].text
        role = "model"

        return response, role, user_input, chat

    except Exception as e:
        return f"Failure: {e}", "model", user_input, chat

def chatting(user_input: str, context: List):
        
    chat = model.start_chat(
            history=context,
        )
    
    try:
        _response = chat.send_message(user_input)
        response = _response.candidates[0].content.parts[0].text
        role = "model"
        
        print("\n\n\n\n\n")
        print(_response)
        print()
        return response, role, user_input, chat

    except Exception as e:
        print(f"Error encountered: {e}")
        return f"Failure: {e}", "model", user_input, chat


def photo_to_product_list(photo_path: str):
    prompt = """
        Analyze the image and provide a list of recognized, standard food products only (e.g., brands or common items like 'Coca-Cola', 'Doritos', 'milk', 'bread', etc.). \n
        Do not include any packaging or unknown items. \n
        For each recognized item, specify the quantity or amount if visible (e.g., '2 bottles of Coca-Cola').\n
        Return the result in a JSON format with the structure:\n
        ```json
        [
        {"product": "<Product Name>", "quantity": "<Amount or Count>"}
        ]
        ```\n
        Important: Only include items that are widely recognized and commonly available; do not invent or add any unknown or generic items.
    """
    myfile = genai.upload_file(f"{photo_path}")
    
    try:
        _response = model.generate_content([myfile, "\n\n", f"{prompt}"])
        response = _response.candidates[0].content.parts[0].text
        role = "user"
        
        # Use regular expression to extract JSON list
        match = re.search(r'(\[.*\])', response, re.DOTALL)

        if match:
            # Extracted JSON string
            json_str = match.group(1)
            
            # Parse the JSON string to a Python object
            response = json.loads(json_str)
            
        else:
            response = [{"None": "None"}]
        
        
        return response, role
        
    
    except Exception as e:
        print(e)
        return str(e), "user"
    
    
def translate(context: str, to_lang: str = "ru_RU") -> str:

    # Perform the translation
    translated_text = translator(context, max_length=1500)[0]['translation_text']
    
    return translated_text