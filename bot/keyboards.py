from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    WebAppInfo, 
    ReplyKeyboardMarkup, 
    KeyboardButton
)

def get_main_keyboard(url):
    """Asosiy pastki menyu (Reply Keyboard)"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍 Do'konni ochish", web_app=WebAppInfo(url=url))]
        ],
        resize_keyboard=True
    )

def get_webapp_keyboard(url):
    """Inline tugma (Xabar tagida)"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛍 Katalogga kirish", web_app=WebAppInfo(url=url))]
    ])

def get_status_keyboard(user_id):
    """Adminlar uchun buyurtma holatini boshqarish tugmasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Holatni yangilash", callback_data=f"status_select:{user_id}")]
    ])

def get_templates_keyboard(user_id):
    """Status shablonlari menyusi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Qabul qilindi", callback_data=f"send_status:{user_id}:accepted")],
        [InlineKeyboardButton(text="👨‍🍳 Tayyorlanmoqda", callback_data=f"send_status:{user_id}:preparing")],
        [InlineKeyboardButton(text="🚚 Yo'lda", callback_data=f"send_status:{user_id}:on_the_way")],
        [InlineKeyboardButton(text="📦 Yetkazildi", callback_data=f"send_status:{user_id}:delivered")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_select")]
    ])
