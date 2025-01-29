import datetime
from enum import StrEnum

# Booking essentials
AVAILABLE_ROOMS = ["Аудитория А", "Аудитория В", "Аудитория С"]
TIMESLOT_DURATION = 30  # in minutes
START_TIME = datetime.time(7, 30)
END_TIME = datetime.time(18, 30)

class BTN_TEXT(StrEnum):
    """
    Button texts.
    """
    CREATE_BOOKING = "📅 Создать бронь"
    MY_BOOKINGS = "📋 Мои бронирования"
    CANCEL = "❌ Отменить"
    CANCELLED = "🟢 Не отменять"
    BACK = "⬅️ Назад"
    FINISH = "✅ Завершить"


class TEXT(StrEnum):
    """
    Static texts.
    """
    ERROR_BOOKING = "<b><i>❌ При бронировании произошла ошибка со стороны бота!</i></b>\nОтчет отправлен администратору."
    ERROR_CANCEL_BOOKING = "<b><i>❌ При отмене бронирования произошла ошибка со стороны бота!</i></b>\nОтчет отправлен администратору."
    SELECT_ROOM = "Выберите аудиторию:"


class TEMPLATE(StrEnum):
    """
    Dynamic texts. To be used with .format() method.
    """
    SELECT_DATE = "Выберите дату брони для <b>{selected_room}</b>:"
    SELECT_TIME = "Выберите время начала и конца брони <b>{selected_room}</b> на <b>{selected_date:%d.%m} ({formatted_day_of_week})</b>:"
    SELECT_TIME_EMPTY = "Нет доступных временных слотов для <b>{selected_room}</b> на <b>{selected_date:%d.%m} ({formatted_day_of_week})</b>."
    SUCCESS_BOOKING = (
        "✅ <b>{room} на {date:%d.%m} ({formatted_day_of_week}), {timeslot} "
        "была забронирована <a href='https://t.me/{username}'>{user_full_name}</a></b>."
    )
    _USER_LINK = "<a href='https://t.me/{user.username}'>{user.full_name}</a>"
    USER_BOOKINGS = "Бронирования пользователя " + _USER_LINK + ":"
    USER_BOOKINGS_EMPTY = "У пользователя " + _USER_LINK + " нет бронирований."
    USER_CANCELED_BOOKINGS = "Пользоывтель " + _USER_LINK + " отменил свои бронирования:"
    USER_CANCELLED = "✅ Пользователь " + _USER_LINK + " отменил:"
    CANCELLED_BOOKING = (
        "<b>{room} на {date:%d.%m} ({formatted_day_of_week}), {timeslot}.</b>"
    )
    REGISTERED_USER = (
        "Пользователь <a href='https://t.me/{user.username}'>{user.full_name}</a> зарегистрирован.\n"
        "<i>Не удаляйте это сообщение.</i>"
    )


class FORMAT(StrEnum):
    """
    Formats (for date and time).
    """
    DATE = "%d.%m"
    TIME = "%H:%M"
