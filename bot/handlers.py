import json
import os
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart
from bot.keyboards import (
    get_status_keyboard, 
    get_templates_keyboard, 
    get_webapp_keyboard, 
    get_main_keyboard
)

logger = logging.getLogger(__name__)
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Start buyrug'i - Media va Katalog tugmalarini yuboradi"""
    photo1 = FSInputFile("bot/assets/kolbasa.png")
    photo2 = FSInputFile("bot/assets/sosiska.png")
    
    media = [
        InputMediaPhoto(
            media=photo1, 
            caption=f"<b>Assalomu alaykum, {message.from_user.full_name}!</b>\n"
                    f"Muxlisa Food onlayn do'koniga xush kelibsiz.\n\n"
                    f"Pastdagi tugmalar orqali katalogimizni ko'rishingiz va buyurtma berishingiz mumkin. 👇"
        ),
        InputMediaPhoto(media=photo2)
    ]
    
    try:
        await message.answer_media_group(media=media)
        
        webapp_url = os.getenv("WEBAPP_URL")
        await message.answer(
            "🛍 Buyurtma berishni boshlash uchun pastdagi tugmani bosing:",
            reply_markup=get_main_keyboard(webapp_url)
        )
    except Exception as e:
        logger.error(f"Error in cmd_start: {e}")

@router.message(F.web_app_data)
async def handle_webapp_data(message: Message, bot: Bot):
    """Mini Appdan kelgan buyurtmani qayta ishlash"""
    try:
        raw_data = message.web_app_data.data
        data = json.loads(raw_data)
        items = data.get('items', [])
        total = data.get('total', 0)
        user_info = data.get('user', {})
        coords = user_info.get('coords') # [lat, lon]
        
        # Mijoz profiliga havola
        user_link = f'<a href="tg://user?id={message.from_user.id}">{user_info.get("name", message.from_user.full_name)}</a>'
        
        # Manzil va Xarita havolasi
        address_text = user_info.get('address', '-')
        if coords and len(coords) == 2:
            lat, lon = coords
            map_link = f"https://yandex.uz/maps/?text={lat},{lon}"
            address_text = f'<a href="{map_link}">{address_text}</a>'

        order_text = (
            f"🆕 <b>Yangi Buyurtma!</b>\n\n"
            f"👤 <b>Mijoz:</b> {user_link}\n"
            f"📞 <b>Tel:</b> <code>{user_info.get('phone', '-')}</code>\n"
            f"📍 <b>Manzil:</b> {address_text}\n"
            f"🆔 <b>User ID:</b> <code>{message.from_user.id}</code>\n\n"
            f"🛒 <b>Mahsulotlar:</b>\n"
        )
        
        for item in items:
            name = item.get('name', 'Noma\'lum')
            qty = item.get('quantity', 1)
            price = item.get('price', 0)
            try:
                price_fmt = f"{int(price):,}"
            except:
                price_fmt = str(price)
            order_text += f"• {name} x{qty} - {price_fmt} so'm\n"
            
        try:
            total_fmt = f"{int(total):,}"
        except:
            total_fmt = str(total)
        order_text += f"\n💰 <b>Jami: {total_fmt} so'm</b>"

        channel_id = os.getenv("CHANNEL_ID")
        if channel_id:
            await bot.send_message(
                chat_id=channel_id,
                text=order_text,
                reply_markup=get_status_keyboard(message.from_user.id)
            )
            
        await message.answer("Sizning buyurtmangiz qabul qilindi! ✅\nTez orada aloqaga chiqamiz.")
        
    except Exception as e:
        logger.error(f"Error in handle_webapp_data: {e}", exc_info=True)
        await message.answer("⚠️ Buyurtmani qayta ishlashda xatolik yuz berdi.")

@router.callback_query(F.data.startswith("status_select:"))
async def select_status(callback: CallbackQuery):
    """Status tanlash menyusini ko'rsatish"""
    user_id = callback.data.split(":")[1]
    await callback.message.edit_reply_markup(
        reply_markup=get_templates_keyboard(user_id)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("status_close:"))
async def close_status_menu(callback: CallbackQuery):
    """Status menyusini yopish (yig'ish)"""
    user_id = callback.data.split(":")[1]
    await callback.message.edit_reply_markup(
        reply_markup=get_status_keyboard(user_id)
    )
    await callback.answer("Menyu yopildi.")

@router.callback_query(F.data.startswith("send_status:"))
async def send_status_to_user(callback: CallbackQuery, bot: Bot):
    """Mijozga holat xabarini yuborish"""
    _, user_id, status_code = callback.data.split(":")
    
    status_messages = {
        "accepted": "✅ Buyurtmangiz qabul qilindi.",
        "preparing": "👨‍🍳 Taomingiz tayyorlanmoqda.",
        "on_the_way": "🚚 Buyurtma yo'lda.",
        "delivered": "📦 Buyurtma yetkazildi. Yoqimli ishtaha!",
        "cancelled": "❌ Uzr, buyurtmangiz bekor qilindi."
    }
    
    msg_text = status_messages.get(status_code, "Holat yangilandi.")
    
    try:
        await bot.send_message(chat_id=user_id, text=msg_text)
        await callback.answer("Mijozga yuborildi! ✅", show_alert=True)
        # Menyuni qayta yopamiz
        await callback.message.edit_reply_markup(
            reply_markup=get_status_keyboard(user_id)
        )
    except Exception as e:
        logger.error(f"Error sending status to user {user_id}: {e}")
        await callback.answer("Xatolik: Mijozga yozib bo'lmadi. ❌", show_alert=True)
