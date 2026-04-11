from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

def get_webapp_keyboard(url):
    """Mini Appni ochish uchun tugma"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🛍 Katalogga kirish", 
                web_app=WebAppInfo(url=url)
            )
        ]
    ])
    return keyboard

def get_status_keyboard(user_id):
    """Kanalda ko'rinadigan 'Holatmi xabar qilish' tugmasi"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔄 Holatni xabarlash", 
                callback_data=f"status_select:{user_id}"
            )
        ]
    ])
    return keyboard

def get_templates_keyboard(user_id):
    """Admin holatni tanlashi uchun tayyor shablonli tugmalar"""
    templates = [
        ("✅ Qabul qilindi", "accepted"),
        ("👨‍🍳 Tayyorlanmoqda", "preparing"),
        ("🚚 Yo'lda", "on_the_way"),
        ("📦 Yetkazildi", "delivered")
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=f"send_status:{user_id}:{code}")]
        for text, code in templates
    ])
    
    # Orqaga tugmasi
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"cancel_select")
    ])
    
    return keyboard
