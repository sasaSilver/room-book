import datetime

# Booking essentials
AVAILABLE_ROOMS = ["Аудитория А", "Аудитория В", "Аудитория С"]
TIMESLOT_DURATION = 30  # in minutes
START_TIME = datetime.time(7, 30)
END_TIME = datetime.time(18, 30)

# Emojis
EMOJI_CROSS = "❌"
EMOJI_GREEN_CIRCLE = "🟢"
EMOJI_RED_CIRCLE = "🔴"
EMOJI_CHECK = "✅"

# Button Text
BTN_CANCEL_TEXT = f"❌ Отменить"
BTN_CANCELLED_TEXT = f"🟢 Не отменять"
BTN_BACK_TEXT = f"⬅️ Назад"
BTN_FINISH_TEXT = f"✅ Завершить"
CREATE_BOOKING_TEXT = "Создать бронь"
MY_BOOKINGS_TEXT = "Мои бронирования"


# Booking dialog texts
SELECT_ROOM_TEXT = "Выберите аудиторию:"
SELECT_DATE_TEMPLATE = "Выберите дату брони для <b>{selected_room}</b>:"
SELECT_TIME_TEMPLATE = "Выберите время начала и конца брони <b>{selected_room}</b> на <b>{selected_date:%d.%m} ({formatted_day_of_week})</b>:"
SELECT_TIME_EMPTY_TEMPLATE = "Нет доступных временных слотов для <b>{selected_room}</b> на <b>{selected_date:%d.%m} ({formatted_day_of_week})</b>."
SUCCESS_BOOKING_TEMPLATE = (
    "✅ <b>{room} на {date:%d.%m} ({formatted_day_of_week}), {timeslot} "
    "была забронирована <a href='https://t.me/{username}'>{user_full_name}</a></b>."
)
ERROR_BOOKING_TEXT = "<b><i>❌ При бронировании произошла ошибка со стороны бота!</i></b>\nОтчет отправлен администратору."

## View bookings dialog texts
_USER_LINK_TEMPLATE = "<a href='https://t.me/{user.username}'>{user.full_name}</a>"
USER_BOOKINGS_TEMPLATE = "Бронирования пользователя " + _USER_LINK_TEMPLATE + ":"
USER_BOOKINGS_EMPTY_TEMPLATE = "У пользователя " + _USER_LINK_TEMPLATE + " нет бронирований."
USER_CANCELED_BOOKINGS_TEMPLATE = "Пользоывтель " + _USER_LINK_TEMPLATE + " отменил свои бронирования:"
SUCCESS_USER_CANCELLED_TEMPLATE = "✅ Пользователь " + _USER_LINK_TEMPLATE + " отменил:"
CANCELLED_BOOKING_TEMPLATE = (
    "<b>{room} на {date:%d.%m} ({formatted_day_of_week}), {timeslot}.</b>"
)
ERROR_CANCEL_BOOKING_TEXT = "<b><i>❌ При отмене бронирования произошла ошибка со стороны бота!</i></b>\nОтчет отправлен администратору."


# Date and time formats
DATE_FORMAT = "%d.%m"
TIME_FORMAT = "%H:%M"

# "Registration" message
WELCOME_MESSAGE_TEMPLATE = (
    "Пользователь <a href='https://t.me/{user.username}'>{user.full_name}</a> зарегистрирован.\n"
    "<i>Не удаляйте это сообщение.</i>"
)
