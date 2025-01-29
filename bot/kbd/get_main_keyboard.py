from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.constants import BTN_TEXT
def get_main_rkeyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BTN_TEXT.CREATE_BOOKING),
                KeyboardButton(text=BTN_TEXT.MY_BOOKINGS)
            ]
        ],
        resize_keyboard=True,
        is_persistent=True,
    )