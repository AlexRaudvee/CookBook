# imports 

import logging
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import BotCommand, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from envvar import BOT_TOKEN
from func import *
from aiogram import F

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

CONTEXT = []
LNG = None

# BUTTONS

# Language Settings
@dp.message(Command("language"))
async def set_language(message: types.Message):    
    buttons = [
        [
            types.InlineKeyboardButton(text="English", callback_data="en"),
            types.InlineKeyboardButton(text="Русский", callback_data="ru")
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await message.answer(
        "Choose the language / Выберите язык:",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "en")
async def lang_change(callback: types.CallbackQuery):
    global LNG
    LNG = 'en'
    await callback.answer()  # Acknowledging the callback
    await callback.message.answer("Language changed to English")
    
@dp.callback_query(F.data == "ru")
async def lang_change(callback: types.CallbackQuery):
    global LNG
    LNG = 'ru'
    await callback.answer()  # Acknowledging the callback
    await callback.message.answer("Язык изменен на Русский")


# COMMANDS


@dp.message(Command("cook"))
async def greeting(message: types.Message):
    
    gret_resp, role = get_gemini_greeting_response()
    
    greeting = "Hi!"
    
    global CONTEXT 
    CONTEXT = []
    
    CONTEXT.append({"role": "user", "parts": [f"{greeting}"]})
    CONTEXT.append({"role": f"{role}", "parts": [f"{gret_resp}"]})
    
    print(CONTEXT)
    
    if LNG == "ru":
        gret_resp = translate(gret_resp)
        
    gret_resp = transform_text(gret_resp)
        
    await message.answer(gret_resp, parse_mode="MarkdownV2")


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    
    en_intro = """*Welcome to CookBook Telegram Bot* \n\nHere is the list of comands that bot supports \\(you can find all of them in the MENU tab\\):\n1\\. /start \\- command that resets the bot and start from the ground \n2\\. /cook \\- start the conversation with the bot \n3\\. /help \\- get the list of all commands \n4\\. /language \\- change the language / сменить язык \n"""
    
    ru_intro = """*Добро пожаловать в CookBook Telegram Бот* \n\nНиже расположены главные команды для начала работы с ботом \\(вы можете найти все команды в вкладке МЕНЮ\\):\n1\\. /start \\- полная перезагрузка бота \n2\\. /cook \\- начать общение с ботом \n3\\. /help \\- получить лист всех доступных комманд \n4\\. /language \\- change the language / сменить язык \n"""
    
    if LNG=='ru':
        prompt = ru_intro
    else: 
        prompt = en_intro
    
    await message.answer(text=prompt, parse_mode="MarkdownV2")

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
    if LNG == 'ru':
        sentence = translate(sentence)
        
    sentence = transform_text(sentence)
        
    await message.answer(sentence, parse_mode="MarkdownV2")
    
    response, role = photo_to_product_list(photo_path)
    
    # return the message to user of what we see on the image
    product_list = [item["product"] for item in response]
    result = ", ".join(product_list)

    sentence = f"Oh, I can see you have: {result}"
    if LNG == "ru":
        sentence = translate(sentence)

    sentence = transform_text(sentence)
        
    await message.answer(sentence, parse_mode="MarkdownV2")
    
    
    # now we send the recipes
    sentence = "Let me see what we can make with these products..."
    if LNG =='ru':
        sentence = translate(sentence)
        
    sentence = transform_text(sentence)
        
    await message.answer(sentence, parse_mode="MarkdownV2")
    
    # if len(CONTEXT) < 4:
    response, role, last_user_message, chat = get_first_recipes(user_input = result, context=CONTEXT)
    
    CONTEXT.append({"role": "user", "parts": [f"{last_user_message}"]})
    CONTEXT.append({"role": f"{role}", "parts": [f"{response}"]})
    
    if LNG == 'ru':
        response = translate(response)
        
    response = transform_text(response)
    
    print(CONTEXT)    
    await message.answer(response, parse_mode="MarkdownV2")
        
    # else: 
    #     print(CONTEXT)
    #     response, role, last_user_message, chat = chatting(user_input = result, context = CONTEXT)
        
    #     CONTEXT.append({"role": "user", "parts": [f"{last_user_message}"]})
    #     CONTEXT.append({"role": f"{role}", "parts": [f"{response}"]})
        
    #     if LNG == 'ru':
    #         response = translate(response)
            
    #     response = transform_text(response)
        
    #     await message.answer(response, parse_mode="MarkdownV2")
    
@dp.message(F.text & ~F.text.startswith('/'))
async def echo(message: types.Message):
    if len(CONTEXT) < 4:
        response, role, last_user_message, chat = get_first_recipes(user_input = message.text, context=CONTEXT)
        
        CONTEXT.append({"role": "user", "parts": [f"{last_user_message}"]})
        CONTEXT.append({"role": f"{role}", "parts": [f"{response}"]})
        
        if LNG == 'ru':
            response = translate(response)
            
        response = transform_text(response)
        
        await message.answer(response, parse_mode="MarkdownV2")
        
    else: 
        print(CONTEXT)
        response, role, last_user_message, chat = chatting(user_input = message.text, context = CONTEXT)
        
        CONTEXT.append({"role": "user", "parts": [f"{last_user_message}"]})
        CONTEXT.append({"role": f"{role}", "parts": [f"{response}"]})
        
        if LNG == 'ru':
            response = translate(response)
            
        response = transform_text(response)
        
        await message.answer(response, parse_mode="MarkdownV2")
        
    print(CONTEXT)
        
async def main():
    
    dp.startup.register
    
    await bot.set_my_commands([
        BotCommand(command="/cook", description="start to chat with the bot"),
        BotCommand(command="/language", description="change the language"),
        BotCommand(command="/start", description="start again"),
    ])
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
