# Emojis
EMOJI_CROSS = "❌"
EMOJI_BACK_ARROW = "⬅️"
EMOJI_GREEN_CIRCLE = "🟢"
EMOJI_RED_CIRCLE = "🔴"
EMOJI_CHECK = "✅"

# Button Text
BTN_CANCEL = f"{EMOJI_CROSS} Отмена"
BTN_BACK = f"{EMOJI_BACK_ARROW} Назад"
CREATE_BOOKING_TEXT = "Создать бронь"
MY_BOOKINGS_TEXT = "Мои бронирования"
BTN_CANCEL_BOOKING = f"{EMOJI_CROSS} Отменить"
BTN_FINISH = f"Завершить {EMOJI_CHECK}"

# Room Names
ROOMS = ["Аудитория А", "Аудитория В", "Аудитория С"]

# Window Headers
HEADER_SELECT_ROOM = "Выберите аудиторию:"
HEADER_SELECT_DATE = "Выберите дату брони для <b>{selected_room}</b>:"
HEADER_SELECT_TIME = "Выберите время начала и конца брони <b>{selected_room}</b> на <b>{selected_date}</b>:"
HEADER_USER_BOOKINGS = "Бронирования пользователя <a href='https://t.me/{user.username}'>{user.full_name}</a>:"
HEADER_NO_BOOKINGS = "У пользователя <a href='https://t.me/{user.username}'>{user.full_name}</a> нет бронирований."

# Error Messages
ERROR_BOT = "<b><i>❌ Произошла ошибка со стороны бота!</i></b>\nОтчет отправлен администратору."
ERROR_DELETE_BOOKING = "<b><i>❌ При удалении бронирования произошла ошибка со стороны бота!</i></b>\nОтчет отправлен администратору."
ERROR_CREATE_BOOKING = "<b><i>❌ При бронировании произошла ошибка со стороны бота!</i></b>\nОтчет отправлен администратору."

# Success Messages
SUCCESS_BOOKING = "✅ <b>{room} на {date}, {timeslot} была забронирована <a href='https://t.me/{username}'>{user_full_name}</a></b>."

# Date and Time Formats
DATE_FORMAT = "%d.%m"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = f"{DATE_FORMAT}, {TIME_FORMAT}"

# Welcome Message
WELCOME_MESSAGE = (
    "Пользователь <a href='https://t.me/{user.username}'>{user.full_name}</a> зарегистрирован.\n"
    "<i>Не удаляйте это сообщение.</i>"
)

