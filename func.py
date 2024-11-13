# imports
import re
import json

import translators as ts
import google.generativeai as genai

from typing import List
from typing_extensions import TypedDict
from tqdm.notebook import tqdm
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from config import model

### CUSTOM FUNCTIONS ###

def transform_text(text: str) -> str:
    
    # Replace single asterisks (*) with '>'
    text = text.replace("* ", "- ")
    # Replace double asterisks (**) with single asterisks (*)
    text = text.replace("**", "*")
    # Place a backslash before specific characters
    characters_to_escape = ["(", ")", "[", "]", "{", "}", "-", ".", "!"]
    for char in characters_to_escape:
        text = text.replace(char, f"\\{char}")
    
    return text

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
        return f"Failure: {e}", role

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
    
    
def translate(context: str, html: bool = False, to_lang: str = "ru") -> str:

    # Perform the translation
    if html:
        translated_text = ts.translate_html(html_text=context, translator='yandex', to_language=to_lang)
    else:
        translated_text = ts.translate_text(query_text=context, translator='yandex', to_language=to_lang)
    
    return translated_text



def stream_get_gemini_greeting_response(user_input: str, context: List):
    prompt = "Hi! Make sure that your greeting response is not longer than 2 sentences."

    # Simulate a generator response (e.g., each part is generated over time)
    try:
        _response = model.generate_content(prompt, stream=True)  # Use `stream=True` if supported

        # This loop would yield chunks of the generated response as they're produced.
        for part in _response:
            yield part.text  # Each part of the response

    except Exception as e:
        yield f"Error encountered: {e}"
    
def stream_get_first_recipes(user_input: str, context: List):
    user_input = f"""You do not have to greet me again! 
                Here is the list of the products that I have: 
                {user_input}. 
                Make sure your response is no longer than 300 words. 
                Give me a list of 3 recipes that I can cook out of this. 
                Give 1 easy and fast recipe, 1 middle difficulty recipe, and 1 vegan recipe. 
                If it is impossible to create a vegan meal out of products you have, give 1 hard difficulty recipe."""
    
    chat = model.start_chat(history=context)
    
    try:
        _response = chat.send_message(user_input)

        # Assuming _response.candidates contain multiple parts to stream incrementally
        for part in _response.candidates[0].content.parts:
            # Yield each part text to stream as it comes
            yield part.text

    except Exception as e:
        yield f"Failure: {e}"

def stream_chatting(user_input: str, context: List):
    # Start a new chat session with the provided context
    chat = model.start_chat(history=context)
    
    # user_input = f"""
    #     If I ask about modification of specific recipe, discuss only recipe that I mention!\n
    #     {user_input}
    # """
    
    try:
        # Send the user input and receive the response as a stream
        _response = chat.send_message(user_input)

        # Assuming _response.candidates[0].content.parts contains multiple parts
        for part in _response.candidates[0].content.parts:
            # Yield each part of the text to stream it
            yield part.text

    except Exception as e:
        yield f"Failure: {e}" 