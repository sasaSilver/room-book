from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.texts import BTN_TEXTS

def get_main_rkeyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BTN_TEXTS.CREATE_BOOKING),
                KeyboardButton(text=BTN_TEXTS.MY_BOOKINGS)
            ]
        ],
        resize_keyboard=True,
        is_persistent=True,
    )