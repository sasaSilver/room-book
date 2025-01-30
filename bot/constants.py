import datetime
from enum import StrEnum

# Booking essentials
AVAILABLE_ROOMS = ["Аудитория А", "Аудитория В", "Аудитория С"]
TIMESLOT_DURATION = 30  # in minutes
START_TIME = datetime.time(7, 30)
END_TIME = datetime.time(18, 30)

class EMOJI(StrEnum):
    TICK = "✅"

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
    ERROR_BOT = "<b><i>❌ Произошла ошибка со стороны бота!</i></b>\nОтчет отправлен администратору."
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
    
class HELP_TEXT(StrEnum):
    """
    Static texts from help dialog.
    """
    CHOOSE_HELP = "Выберите, с чем нужна помощь:"
    
    HOW2_MENU = "Почему нет меню бота?"
    HOW2_BOOK = "Как забронировать?"
    HOW2_VIEW = "Как посмотреть свои брони?"
    HOW2_VIEW_ALL = "Как просмотреть все брони?"
    HOW2_CANCEL = "Как отменить свою бронь?"
    MENU = (
        "Меню находится под полем ввода текста телеграма.\n\n"
        "Если его не видно, в поле ввода нажмите на самую правую квадратную иконку.\n\n"
        "Если нет иконки, отправьте <i>/start</i>."
    )
    BOOK = (
        "1. Нажмите на <i>\"Создать бронь\"</i> в меню бота."
        "2. Выберите аудиторию, которую желаете забронировать.\n\n"
        "3. Выберите дату в календаре. В календаре можно просматривать любые месяца, нажав на кнопки со стрелками снизу по бокам.\n\n"
        "4. Выберите время начала и конца брони, нажав сначала на время начала, затем на время конца.\n\n"
        "5. После выбора времени, появится кнопка <i>\"Завершить\"</i>. Нажмите на нее, чтобы создать бронь."
    )
    VIEW = (
        "1. Нажмите на <i>\"Мои бронирования\"</i> в меню бота."
        "2. В выведенном списке покажутся страницы со всеми бронями, которые переключаются стрелками."
    )
    VIEW_ALL = (
        "Нажмите на <i>\"Все брони\"</i> в меню бота. Если у вас нет меню, отправьте команду <i>\"/start\"</i>."
    )
    CANCEL = (
        "1. Просмотрите свои брони.\n\n"
        "2. Кнопка отмены на странице с бронью позволяет выбрать, отменить или не отменять текущую бронь. "
        "Если была выбрана отмена, после нажатия кнопки <i>\"Завершить\"</i> бронь отменится."
    )