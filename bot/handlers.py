import json
import os
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSFile, InputMediaPhoto
from aiogram.filters import CommandStart
from bot.keyboards import get_status_keyboard, get_templates_keyboard, get_webapp_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Start buyrug'i - Media Group va Mini App tugmasini yuboradi"""
    # Rasmlar yo'llari
    photo1 = FSFile("bot/assets/kolbasa.png")
    photo2 = FSFile("bot/assets/sosiska.png")
    
    # Media guruhi
    media = [
        InputMediaPhoto(media=photo1, caption=f"Assalomu alaykum, {message.from_user.full_name}!\nMuxlisa Food onlayn do'koniga xush kelibsiz.\n\nPastdagi tugma orqali katalogimizni ko'rishingiz mumkin. 👇"),
        InputMediaPhoto(media=photo2)
    ]
    
    # Rasmlarni yuborish
    await message.answer_media_group(media=media)
    
    # Tugmani alohida yuborish (Media guruhi bilan birga tugma yuborib bo'lmaydi)
    webapp_url = os.getenv("WEBAPP_URL")
    await message.answer(
        "Buyurtma berishni boshlang:",
        reply_markup=get_webapp_keyboard(webapp_url)
    )

@router.message(F.web_app_data)
async def handle_webapp_data(message: Message, bot: Bot):
    """Mini Appdan kelgan buyurtmani qabul qilish va kanalga yuborish"""
    try:
        data = json.loads(message.web_app_data.data)
        items = data.get('cart', [])
        total = data.get('total', 0)
        
        # Buyurtma matnini shakllantirish
        order_text = f"🆕 **Yangi Buyurtma!**\n\n"
        order_text += f"👤 Mijoz: {message.from_user.full_name}\n"
        order_text += f"🆔 User ID: `{message.from_user.id}`\n\n"
        order_text += "🛒 Mahsulotlar:\n"
        
        for item in items:
            order_text += f"- {item['name']} x{item['quantity']} ({item['price']:,} so'm)\n"
            
        order_text += f"\n💰 **Jami: {total:,} so'm**"

        # Kanalga yuborish
        channel_id = os.getenv("CHANNEL_ID")
        if channel_id:
            await bot.send_message(
                chat_id=channel_id,
                text=order_text,
                reply_markup=get_status_keyboard(message.from_user.id)
            )
            
        await message.answer("Buyurtmangiz qabul qilindi! Tezz orada aloqaga chiqamiz. ✅")
        
    except Exception as e:
        print(f"Error handling webapp data: {e}")
        await message.answer("Buyurtmani qayta ishlashda xatolik yuz berdi. ❌")

@router.callback_query(F.data.startswith("status_select:"))
async def select_status(callback: CallbackQuery):
    """Admin holatni tanlashi uchun shablonlarni ko'rsatish"""
    user_id = callback.data.split(":")[1]
    await callback.message.edit_reply_markup(
        reply_markup=get_templates_keyboard(user_id)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("send_status:"))
async def send_status_to_user(callback: CallbackQuery, bot: Bot):
    """Tanlangan shablonni mijozga yuborish"""
    _, user_id, status_code = callback.data.split(":")
    
    status_messages = {
        "accepted": "✅ Buyurtmangiz qabul qilindi.",
        "preparing": "👨‍🍳 Taomingiz tayyorlanmoqda.",
        "on_the_way": "🚚 Buyurtma yo'lda, kuryerimiz yaqinlashmoqda.",
        "delivered": "📦 Buyurtma yetkazib berildi. Yoqimli ishtaha!"
    }
    
    msg_text = status_messages.get(status_code, "Holat yangilandi.")
    
    try:
        await bot.send_message(chat_id=user_id, text=msg_text)
        await callback.answer(f"Xabar mijozga yuborildi! ✅", show_alert=True)
        # Kanalda tugmani qayta tiklash
        await callback.message.edit_reply_markup(
            reply_markup=get_status_keyboard(user_id)
        )
    except Exception as e:
        await callback.answer(f"Xatolik: Mijozga yozib bo'lmadi. ❌", show_alert=True)

@router.callback_query(F.data == "cancel_select")
async def cancel_selection(callback: CallbackQuery):
    """Tanlovni bekor qilish"""
    # Bu yerda user_id ni callback_query xabaridan olish qiyinroq bo'lishi mumkin 
    # shuning uchun callback_data da saqlagan ma'qul edi. 
    # Hozircha shunchaki yopamiz.
    await callback.answer("Bekor qilindi.")
