import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot.handlers import router

# .env faylini yuklash
load_dotenv()

async def main():
    # Logging sozlamalari
    logging.basicConfig(level=logging.INFO)
    
    # Bot obyektini yaratish
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        print("Xatolik: BOT_TOKEN topilmadi. .env faylini tekshiring.")
        return

    bot = Bot(token=bot_token)
    dp = Dispatcher()
    
    # Routerni qo'shish
    dp.include_router(router)
    
    print("Bot ishga tushdi... 🚀")
    
    # Pollingni boshlash
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
