import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.handlers import router

# .env faylini yuklash
load_dotenv()

async def main():
    # Logging sozlamalari (Professional darajadagi format)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Bot obyektini yaratish
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logger.error("BOT_TOKEN topilmadi! .env faylini tekshiring.")
        return

    # Botni universal sozlamalar bilan yaratish (ParseMode HTML)
    bot = Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Routerni qo'shish
    dp.include_router(router)
    
    logger.info("Bot ishga tushdi... 🚀")
    
    try:
        # Eski update'larni o'chirib yuborish (Bot tezroq ulanishi uchun)
        await bot.delete_webhook(drop_pending_updates=True)
        # Pollingni boshlash
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Botni yurgizishda xatolik: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
