# imports 

import logging
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from envvar import BOT_TOKEN
from func import *

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

CONTEXT = []
lng = 'en'

# Create inline keyboard button for /start
def get_start_button():
    start_button = InlineKeyboardButton(text="Start", callback_data="/start")
    keyboard = InlineKeyboardMarkup([[start_button]])
    return keyboard

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    
    gret_resp, role = get_gemini_greeting_response()
    
    greeting = "Hi!"
    
    CONTEXT.append({"role": "user", "parts": [f"{greeting}"]})
    CONTEXT.append({"role": f"{role}", "parts": [f"{gret_resp}"]})
    
    print(CONTEXT)
    
    if lng == "ru":
        gret_resp = translate(gret_resp)
        
    await message.answer(gret_resp)

# Handler for photo messages
@dp.message(lambda message: message.photo)
async def handle_photo(message: types.Message):
    # Get the highest resolution photo
    photo = message.photo[-1]
    
    # Get the file information
    file_info = await bot.get_file(photo.file_id)
    
    # Download the file and save it as "photo.png"
    photo_path = "photo.png"
    await bot.download_file(file_info.file_path, destination=photo_path)
    
    # get the json list of the products
    sentence = "Let me see what we have here..."
    if lng == 'ru':
        sentence = translate(sentence)
        
    await message.answer(sentence)
    
    response, role = photo_to_product_list(photo_path)
    

    # return the message to user of what we see on the image
    product_list = [item["product"] for item in response]
    result = ", ".join(product_list)

    sentence = f"Oh, I can see you have: {result}"
    if lng == "ru":
        sentence = translate(sentence)
        
    await message.answer(sentence)
    
    
    # now we send the recipes
    sentence = "Let me see what we can make with these products..."
    if lng =='ru':
        sentence = translate(sentence)
        
    await message.answer(sentence)
    
    if len(CONTEXT) < 4:
        response, role, last_user_message, chat = get_first_recipes(user_input = result, context=CONTEXT)
        
        CONTEXT.append({"role": "user", "parts": [f"{last_user_message}"]})
        CONTEXT.append({"role": f"{role}", "parts": [f"{response}"]})
        
        if lng == 'ru':
            response = translate(response)
        
        await message.answer(response)
        
    else: 
        print(CONTEXT)
        response, role, last_user_message, chat = chatting(user_input = result, context = CONTEXT)
        
        CONTEXT.append({"role": "user", "parts": [f"{last_user_message}"]})
        CONTEXT.append({"role": f"{role}", "parts": [f"{response}"]})
        
        if lng == 'ru':
            response = translate(response)
        
        await message.answer(response)
    
@dp.message()
async def echo(message: types.Message):
    if len(CONTEXT) < 4:
        response, role, last_user_message, chat = get_first_recipes(user_input = message.text, context=CONTEXT)
        
        CONTEXT.append({"role": "user", "parts": [f"{last_user_message}"]})
        CONTEXT.append({"role": f"{role}", "parts": [f"{response}"]})
        
        if lng == 'ru':
            response = translate(response)
        
        await message.answer(response)
        
    else: 
        print(CONTEXT)
        response, role, last_user_message, chat = chatting(user_input = message.text, context = CONTEXT)
        
        CONTEXT.append({"role": "user", "parts": [f"{last_user_message}"]})
        CONTEXT.append({"role": f"{role}", "parts": [f"{response}"]})
        
        if lng == 'ru':
            response = translate(response)
        
        await message.answer(response)
        
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
