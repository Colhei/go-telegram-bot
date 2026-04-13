import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.filters.command import CommandObject
from dotenv import load_dotenv
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from game import *

# завантажуємо змінні з .env
load_dotenv()
TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Бот працює ✅")

@dp.message(Command("play"))
async def start_game(message: types.Message):
    Start_game()
    print("\ntable generating request sent")
    await message.answer("Гру створено")
    await message.answer(Print_table())

@dp.message(Command("duel"))
async def to_challenge(message: types.Message, command: CommandObject):
    player1 = command.args
    player2 = "@" + message.from_user.username            # гравець 1 - отримувач, гравець 2 - відправник
    print(f"\nduel request pending. \nplayers: 1 - {player1} 2 - {player2}")
    To_challenge(player1, player2)
    await message.answer(f"{player2} кидає виклик {player1}")

@dp.message(Command("accept"))
async def accept_duel_request(message: types.Message, command: CommandObject):
    player1 = "@" + message.from_user.username
    player2 = command.args
    print(f"accepting duel requested to game script. {player1} is trying to accept {player2}'s request.")
    result = Accept_duel_request(player1, player2)
    if result:
        print(f"player {player1} accepting {player2}'s duel request")
        await message.answer(f"{player1} приймає виклик {player2}")
    else:
        print(f"player {player1} is trying to accept {player2}'s duel request but no result")
        await message.answer(f"Не вдалося прийняти виклик")

@dp.message(Command("check_games"))
async def check_pending_games(message: types.Message):
    print("started checking pending games.")
    result = Check_pending_games()
    if result:
        print("checking pending games function found some results, they are sent by bot")
        await message.answer(result)
    else:
        print("checking pending games function did not find any pending game")
        await message.answer("Не знайдено жодної гри")

@dp.message(Command("check_requests"))
async def check_pending_requests(message: types.Message):
    print("started checking pending duel requests.")
    result = Check_pending_requests()
    if result:
        print("checking pending duel requests function found some results, they are sent by bot")
        await message.answer(result)
    else:
        print("checking pending duel requests function did not find any pending requests")
        await message.answer(result)

@dp.message(Command("move"))
async def make_move(message: types.Message):
    pass

async def on_startup():
    print("Bot is ready for work 🚀")

async def main():
    print("Bot has started")
    await dp.start_polling(bot, on_startup=on_startup)
    print("Bot has stopped")

if __name__ == "__main__":
    asyncio.run(main())
