import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class Cell:
    __init__(self, status="cross", color="blank", coordx, coordy)):
        self.status = status
        self.color = color
        self.coord = (coordx, coordy)

    def return_color():
        return self.color

    def return_status():
        return self.status

class Game:
    __init__(self):
        self.players = {
                "player1": "",
                "player2": "",
                }


# завантажуємо змінні з .env
load_dotenv()
TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Бот працює ✅")

@dp.message(Command("play"))
async def start_handler(message: types.Message):
    pass

async def on_startup():
    print("Бот готовий до роботи 🚀")

async def main():
    print("Бот запустився")
    await dp.start_polling(bot, on_startup=on_startup)
    print("Бота зупинено")

if __name__ == "__main__":
    asyncio.run(main())
