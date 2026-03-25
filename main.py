import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class Cell:
    __init__(self, status="cross", color="blank", coordx, coordy, available=True)):
        self.status = status
        self.color = color
        self.coord = (coordx, coordy)
        self.available = available

    def return_info(info):
        match info:
            case "coord":
                return self.coord
            case "color":
                return self.color
            case "status":
                return self.status
            case "available":
                return self.available
            case _:
                return None


class Game:
    __init__(self, player1="", player2=""):
        self.players = {
                "player1": player1,
                "player2": player2,
                }
        self.table = [] 

    def generate_table(table_size=9):
        for i in range(table_size):
            self.table.append([])
        for i in range(table_size):
            for j in range(table_size):
                self.table[i].append(Cell())

    def show_table():
        result = f"⏹️1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣/n"       #тут координати стовпців у вигляді емоджі
        for i in range(len(self.table)):
            match i:
                case 0:
                    result += "9️⃣"   #9
                case 1:
                    result += "8️⃣"   #8
                case 2:
                    result += "7️⃣"   #7
                case 3:
                    result += "6️⃣"   #6
                case 4:                         #тут додається нумерація для рядків
                    result += "5️⃣"   #5
                case 5:
                    result += "4️⃣"   #4
                case 6:
                    result += "3️⃣"   #3
                case 7:
                    result += "2️⃣"   #2
                case 8:
                    result += "1️⃣"   #1
                
            for item in self.table[i]:
                if item.color = "blank":
                    result += "➕"
                elif item.color = "white":
                    result += "⚪️"
                elif item.color = "black":
                    result += "⚫️"
                else:
                    result += "|"

            result += "/n"
        return result

# завантажуємо змінні з .env
load_dotenv()
TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
GAME = Game()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Бот працює ✅")

@dp.message(Command("play"))
async def start_handler(message: types.Message):
    await message.answer("Гра запускається...")
    GAME.generate_table()
    await message.answer("Гру створено.")
    await message.answer("Виводиться стіл...")
    await message.answer(GAME.show_table())

async def on_startup():
    print("Бот готовий до роботи 🚀")

async def main():
    print("Бот запустився")
    await dp.start_polling(bot, on_startup=on_startup)
    print("Бота зупинено")

if __name__ == "__main__":
    asyncio.run(main())
