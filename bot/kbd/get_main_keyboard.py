from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_rkeyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Создать бронь"),
                KeyboardButton(text="Мои бронирования")
            ]
        ],
        resize_keyboard=True,
        persistent=True
    )