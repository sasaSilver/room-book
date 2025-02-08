import datetime

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format, Case
from aiogram_dialog.widgets.kbd import (
    Button,
    Row,
    Calendar,
    CalendarConfig,
    Group,
    Back,
)

from aiogram.types import CallbackQuery, User
from aiogram.fsm.state import State, StatesGroup
from aiogram import F


from bot import settings
from bot.widgets import TimeRangeCustom, CancelCustom
import bot.database.db_op as db_op
from bot.database.schemas import BookingSchema
from bot.utils.utils import (
    generate_timeslots,
    to_timeslot_str,
    get_time_selection_state,
    TimeWindowState,
)
from bot.texts import EMOJIS, CONST, TEMPLATES, BTN_TEXTS


class BookingDialogStates(StatesGroup):
    SELECT_ROOM = State()
    SELECT_DATE = State()
    SELECT_BOOKING_TIME = State()


async def select_room(
    _callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data["selected_room"] = button.text.text
    await dialog_manager.switch_to(BookingDialogStates.SELECT_DATE)


async def select_date(
    callback: CallbackQuery,
    _calendar: Calendar,
    dialog_manager: DialogManager,
    selected_date: datetime.date,
):
    dialog_manager.dialog_data["selected_date"] = selected_date
    await dialog_manager.switch_to(BookingDialogStates.SELECT_BOOKING_TIME)
    callback.message.delete()


async def create_booking(
    callback: CallbackQuery, _button, dialog_manager: DialogManager
):
    data = dialog_manager.dialog_data
    user: User = dialog_manager.event.from_user

    booking = BookingSchema(
        username=user.username,
        user_full_name=user.full_name,
        room=data["selected_room"],
        date=data["selected_date"],
        start_time=datetime.time.fromisoformat(data["start_time"]),
        end_time=datetime.time.fromisoformat(data["end_time"]),
    )

    await db_op.create_booking(booking)

    await dialog_manager.done(result=booking)
    await callback.answer(EMOJIS.TICK)
    await callback.message.delete()


async def clear_date_time_cache(_callback, _button, dm: DialogManager):
    time_selection_widget: TimeRangeCustom = dm.find("time_selection")
    time_selection_widget.reset(dm)
    dm.dialog_data.pop("start_time", None)
    dm.dialog_data.pop("end_time", None)
    dm.dialog_data.pop("cached_bookings", None)


async def get_selected_room(dialog_manager: DialogManager, **_kwargs):
    room = dialog_manager.dialog_data["selected_room"]
    return {"room": room}


async def get_time_selection_data(**kwargs):
    dm: DialogManager = kwargs["dialog_manager"]
    data = dm.dialog_data
    partial_result = {
        "date": data["selected_date"],
        "day_of_week": data["selected_date"].strftime("%a"),
        "room": data["selected_room"],
        "time_selection_state": get_time_selection_state(dm),
        "timeslot": to_timeslot_str(*dm.find("time_selection").get_widget_data(dm, [])),
        "daily_bookings": None,
    }

    if "cached_bookings" in data:
        partial_result["daily_bookings"] = data["cached_bookings"]
        return partial_result

    daily_bookings = await db_op.get_bookings_by_date_room(
        data["selected_date"], data["selected_room"]
    )

    partial_result["daily_bookings"] = daily_bookings
    dm.dialog_data["cached_bookings"] = daily_bookings
    # store fetched bookings as "cache" in dialog data
    # to not refetch on window re-render
    return partial_result


select_room_window = Window(
    Const(CONST.SELECT_ROOM),
    *[
        Button(Const(room), id=f"btn_room_{i}", on_click=select_room)
        for i, room in enumerate(settings.rooms)
    ],
    CancelCustom(Const(BTN_TEXTS.CLOSE)),
    state=BookingDialogStates.SELECT_ROOM,
)

select_date_window = Window(
    Format(TEMPLATES.SELECT_DATE),
    Calendar(
        id="calendar",
        on_click=select_date,
        config=CalendarConfig(min_date=datetime.date.today()),
    ),
    Row(
        Back(Const(BTN_TEXTS.BACK)),
        CancelCustom(Const(BTN_TEXTS.CLOSE)),
    ),
    getter=get_selected_room,
    state=BookingDialogStates.SELECT_DATE,
)

select_time_window = Window(
    Case(
        {
            TimeWindowState.NO_TIMESLOTS: Format(TEMPLATES.SELECT_TIME_EMPTY),
            TimeWindowState.HAS_TIMESLOTS: Format(TEMPLATES.SELECT_START_TIME),
            TimeWindowState.SELECTED_START_TIME: Format(TEMPLATES.SELECT_END_TIME),
            TimeWindowState.SELECTED_END_TIME: Format(TEMPLATES.CONFIRM_BOOKING),
        },
        selector="time_selection_state",
    ),
    Group(
        TimeRangeCustom(
            timepoints=generate_timeslots(
                settings.start_time, settings.end_time, settings.timeslot_duration
            ),
            id="time_selection",
        ),
        width=4,
    ),
    Row(
        Back(Const(BTN_TEXTS.BACK), on_click=clear_date_time_cache),
        Button(
            Const(BTN_TEXTS.FINISH),
            id="btn_time_selected",
            on_click=create_booking,
            when=F["dialog_data"]["start_time"] and F["dialog_data"]["end_time"],
        ),
    ),
    CancelCustom(Const(BTN_TEXTS.CLOSE)),
    state=BookingDialogStates.SELECT_BOOKING_TIME,
    getter=get_time_selection_data,
)


async def send_booking_confirmation(result: BookingSchema | None, dm: DialogManager):
    if result is None:
        return

    booking = result
    timeslot_text = to_timeslot_str(booking.start_time, booking.end_time)
    await dm.event.message.answer(
        TEMPLATES.SUCCESS_BOOKING.format(
            room=booking.room,
            date=booking.date,
            day_of_week=booking.date.strftime("%a"),
            timeslot=timeslot_text,
            user=dm.event.from_user,
        )
    )


booking_dialog = Dialog(
    select_room_window,
    select_date_window,
    select_time_window,
    on_close=send_booking_confirmation,
)
