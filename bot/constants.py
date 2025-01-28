import datetime

# Emojis
EMOJI_CROSS = "❌"
EMOJI_GREEN_CIRCLE = "🟢"
EMOJI_RED_CIRCLE = "🔴"
EMOJI_CHECK = "✅"

# Button Text
BTN_CANCEL = f"❌ Отмена"
BTN_BACK = f"⬅️ Назад"
BTN_FINISH = f"✅ Завершить"
CREATE_BOOKING_TEXT = "Создать бронь"
MY_BOOKINGS_TEXT = "Мои бронирования"

# Room Names
ROOMS = ["Аудитория А", "Аудитория В", "Аудитория С"]

# Window Headers
HEADER_SELECT_ROOM = "Выберите аудиторию:"
HEADER_SELECT_DATE = "Выберите дату брони для <b>{selected_room}</b>:"
HEADER_SELECT_TIME = "Выберите время начала и конца брони <b>{selected_room}</b> на <b>{selected_date:%d.%m} ({formatted_day_of_week})</b>:"
HEADER_SELECT_TIME_EMPTY = "Нет доступных временных слотов для <b>{selected_room}</b> на <b>{selected_date:%d.%m} ({formatted_day_of_week})</b>."
HEADER_USER_BOOKINGS = "Бронирования пользователя <a href='https://t.me/{user.username}'>{user.full_name}</a>:"
HEADER_USER_BOOKINGS_EMPTY = "У пользователя <a href='https://t.me/{user.username}'>{user.full_name}</a> нет бронирований."

# Error Messages
ERROR_BOT = "<b><i>❌ Произошла ошибка со стороны бота!</i></b>\nОтчет отправлен администратору."
ERROR_DELETE_BOOKING = "<b><i>❌ При удалении бронирования произошла ошибка со стороны бота!</i></b>\nОтчет отправлен администратору."
ERROR_CREATE_BOOKING = "<b><i>❌ При бронировании произошла ошибка со стороны бота!</i></b>\nОтчет отправлен администратору."

# Success Messages
SUCCESS_BOOKING = "✅ <b>{room} на {date:%d.%m} ({formatted_day_of_week}), {timeslot} была забронирована <a href='https://t.me/{username}'>{user_full_name}</a></b>."

# Date and Time Formats
DATE_FORMAT = "%d.%m"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = f"{DATE_FORMAT}, {TIME_FORMAT}"

# Welcome Message
WELCOME_MESSAGE = (
    "Пользователь <a href='https://t.me/{user.username}'>{user.full_name}</a> зарегистрирован.\n"
    "<i>Не удаляйте это сообщение.</i>"
)

# Booking time endpoints
START_TIME = datetime.time(7, 30)
END_TIME = datetime.time(18, 30)
