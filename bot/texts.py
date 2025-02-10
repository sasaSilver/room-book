from enum import StrEnum
from bot.settings import settings

class EMOJIS(StrEnum):
    TICK = "✅"


class BTNS(StrEnum):
    """
    Button texts.
    """
    # Main menu KeyboardButtons
    CREATE_BOOKING = "📅 Создать бронь"
    MY_BOOKINGS = "👤 Мои брони"
    BOOKINGS_SCHEDULE = "🖼️ Расписание броней"
    
    # InlineKeyboardButtons
    CLOSE = "❌ Закрыть"
    BACK = "⬅️ Назад"
    FINISH = "✅ Завершить"
    CANCEL_BOOKING = "🔴 Отменить бронь"
    CANCELLED = "🟢 Не отменять"


class CONST(StrEnum):
    """
    Static strings.
    """
    ERROR_BOT = "<b><i>❌ Произошла ошибка со стороны бота!</i></b>\nОтчет отправлен администратору."
    SELECT_ROOM = "Выберите аудиторию:"
    URL_PREFIX = "schedule"
    SCHEDULE_URL_PATTERN = r"^{}://(.*?)___".format(URL_PREFIX)


class TEMPLATES(StrEnum):
    """
    Dynamic strings. To be used with .format() method.
    """
    SELECT_DATE = "Выберите дату брони для <b>{room}</b>:"
    SELECT_TIME_EMPTY = "Нет доступных временных слотов для <b>{room}</b> на <b>{date:%d.%m} ({day_of_week})</b>."
    SELECT_START_TIME = "Выберите время начала брони <b>{room}</b> на <b>{date:%d.%m} ({day_of_week})</b>:"
    SELECT_END_TIME = SELECT_START_TIME.replace("начала", "конца")
    CONFIRM_BOOKING = "Подтвердите бронь: <b>{room}</b> на <b>{date:%d.%m} ({day_of_week}), {timeslot}</b>"
    USER_LINK = "<a href='https://t.me/{user.username}'>{user.full_name}</a>"
    SUCCESS_BOOKING = (
        "✅ <b>{room} на {date:%d.%m} ({day_of_week}), {timeslot} "
        "была забронирована " + USER_LINK + "</b>."
    )
    USER_BOOKINGS = "Бронирования пользователя " + USER_LINK + ":"
    USER_BOOKINGS_EMPTY = "У пользователя " + USER_LINK + " нет бронирований."
    USER_CANCELED_BOOKINGS = "Пользоывтель " + USER_LINK + " отменил свои бронирования:"
    USER_CANCELLED = "✅ Пользователь " + USER_LINK + " отменил:"
    CANCELLED_BOOKING = "<b>{room} на {date:%d.%m} ({day_of_week}), {timeslot}.</b>"
    BOOKINGS_VIEW = "Все бронирования{for_room}:"
    VIEW_EMPTY = "Бронирования отутствуют."
    REGISTERED_USER = (
        "Пользователь " + USER_LINK + " зарегистрирован.\n"
        "<i>Не удаляйте это сообщение.</i>"
    )
    SCHEDULE_URL = "schedule://{date_iso}___{context_id}"


class FORMATS(StrEnum):
    """
    Formats (for date and time).
    """
    DATE = "%d.%m"
    TIME = "%H:%M"


class HELPS(StrEnum):
    """
    Static texts from help dialog.
    """
    CHOOSE_HELP = "Выберите, с чем нужна помощь:"

    HOW2_MENU = "Почему нет меню бота?"
    HOW2_BOOK = "Как забронировать?"
    HOW2_VIEW = "Как посмотреть свои брони?"
    HOW2_VIEW_ALL = "Как просмотреть все брони?"
    HOW2_CANCEL = "Как отменить свою бронь?"
    WHY_BOT_DOWN = "Почему не видно бронирования?"
    
    MENU = f"<b>{HOW2_MENU}</b>\n\n" + (
        "Меню находится под полем ввода текста телеграма.\n\n"
        "Если его не видно, в поле ввода нажмите на самую правую квадратную иконку.\n\n"
        "Если нет иконки, отправьте <i>/start</i>."
    )
    BOOK = f"<b>{HOW2_BOOK}</b>\n\n" + (
        '1. Нажмите на <i>"Создать бронь"</i> в меню бота.\n\n'
        "2. Выберите аудиторию, которую желаете забронировать.\n\n"
        "3. Выберите дату в календаре. В календаре можно просматривать "
        "любые месяца, нажав на кнопки со стрелками снизу по бокам.\n\n"
        "4. Выберите время начала и конца брони, нажав сначала на время начала, "
        "затем на время конца.\n\n"
        "5. После выбора времени, появится кнопка <i>\"Завершить\"</i>. "
        "Нажмите на нее, чтобы создать бронь."
    )
    VIEW = f"<b>{HOW2_VIEW}</b>\n\n" + (
        '1. Нажмите на <i>"Мои бронирования"</i> в меню бота.\n\n'
        "2. В выведенном списке покажутся страницы со всеми бронями, "
        "которые переключаются стрелками."
    )
    VIEW_ALL = f"<b>{HOW2_VIEW_ALL}</b>\n\n" + (
        'Нажмите на <i>"Все брони"</i> в меню бота.'
    )
    CANCEL = f"<b>{HOW2_CANCEL}</b>\n\n" + (
        "1. Просмотрите свои брони.\n\n"
        "2. Кнопка отмены на странице с бронью позволяет выбрать, "
        "отменить или не отменять текущую бронь. "
        "Если была выбрана отмена, после нажатия кнопки "
        "<i>\"Завершить\"</i> бронь отменится."
    )
    BOT_DOWN = f"<b>{WHY_BOT_DOWN}</b>\n\n" + (
        "Некоторые запросы могут долго обрабатываться. "
        "Если бот вообще не отвечает на некоторые сообщения, сообщите "
        f"<a href='https://t.me/{settings.adm_username}'>администратору</a>."
    )
