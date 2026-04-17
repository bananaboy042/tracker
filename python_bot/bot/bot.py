from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

BOT_TOKEN = "8122014475:AAFvhPjFOkzBB0FSM-e-A6P9jaUIHU52KF4"

# Используем альтернативный домен (полный URL)
API_URL = "https://telegg.ooo/bot{}/{}"

bot = Bot(token=BOT_TOKEN, base_url=API_URL)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Бот работает!")

async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())