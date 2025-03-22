import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from telethon import TelegramClient

# 🔹 Данные от BotFather
BOT_TOKEN = "ВАШ_ТОКЕН_БОТА"

# 🔹 Данные от my.telegram.org
API_ID = 123456  # Ваш API ID
API_HASH = "abcdef1234567890abcdef1234567890"
PHONE_NUMBER = "+1234567890"

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Клавиатура
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("✅ Включить онлайн"), KeyboardButton("❌ Выключить онлайн"))

# Телеграм-клиент для управления аккаунтом
client = TelegramClient("session", API_ID, API_HASH)

# Флаг состояния онлайна
is_online = False

async def stay_online():
    global is_online
    async with client:
        await client.start(PHONE_NUMBER)
        while is_online:
            await client.send_message("me", "👋 Я онлайн!")
            await asyncio.sleep(300)

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.reply("👋 Привет! Управляй онлайном с кнопками ниже:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "✅ Включить онлайн")
async def enable_online(message: types.Message):
    global is_online
    if not is_online:
        is_online = True
        asyncio.create_task(stay_online())
        await message.reply("✅ Вечный онлайн включен!")
    else:
        await message.reply("⚡ Уже включено!")

@dp.message_handler(lambda message: message.text == "❌ Выключить онлайн")
async def disable_online(message: types.Message):
    global is_online
    if is_online:
        is_online = False
        await message.reply("❌ Вечный онлайн выключен!")
    else:
        await message.reply("⚡ Уже выключено!")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.connect())  
    executor.start_polling(dp, skip_updates=True)
