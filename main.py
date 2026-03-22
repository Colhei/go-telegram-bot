import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# завантажуємо змінні з .env
load_dotenv()
TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Бот працює ✅")

@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(f"Ти написав: {message.text}")

async def on_startup():
    print("Бот готовий до роботи 🚀")

async def main():
    print("Бот запустився")
    await dp.start_polling(bot, on_startup=on_startup)
    print("Бота зупинено")

if __name__ == "__main__":
    asyncio.run(main())
