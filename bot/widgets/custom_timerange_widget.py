

import datetime
from typing import TypedDict, assert_never

from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog import DialogManager, DialogProtocol
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Keyboard

class Booking(TypedDict):
    id: int
    user_id: int
    user_alias: str
    time_start: str
    time_end: str

class TimeRangeWidget(Keyboard):
    """
    Widget for time selection: 07:00, 07:30, 08:00, ...
    """

    def reset(self, manager: DialogManager):
        self.set_widget_data(manager, [])

    def get_all_time_points(self) -> list[datetime.time]:
        return self.timepoints

    def get_end_time_points(self, start_time: datetime.time) -> list[datetime.time]:
        timepoints = self.get_all_time_points()
        start_index = timepoints.index(start_time)
        return timepoints[start_index:]

    def get_already_booked_timepoints(
        self, daily_bookings: list[Booking], reverse: bool = False
    ) -> dict[datetime.time, Booking]:
        already_booked_timepoints: dict[datetime.time, Booking] = {}
        for timeslot in self.timepoints:
            for booking in daily_bookings:
                time_start = datetime.datetime.fromisoformat(booking["time_start"])
                time_end = datetime.datetime.fromisoformat(booking["time_end"])

                if not reverse and time_start.time() <= timeslot < time_end.time():
                    already_booked_timepoints[timeslot] = booking
                    break
                if reverse and time_start.time() < timeslot <= time_end.time():
                    already_booked_timepoints[timeslot] = booking
                    break
        return already_booked_timepoints

    def get_blocked_timepoints(
        self, selected_time: datetime.time | None, daily_bookings: list[Booking]
    ) -> list[datetime.time]:
        blocked_timepoints = []

        for timepoint in self.timepoints:
            for booking in daily_bookings:
                booking_start_time = datetime.datetime.fromisoformat(booking["time_start"]).time()
                booking_end_time = datetime.datetime.fromisoformat(booking["time_end"]).time()
                if selected_time is None:
                    if booking_start_time <= timepoint < booking_end_time:
                        blocked_timepoints.append(timepoint)
                        break
                elif not (
                    (booking_start_time < selected_time and booking_end_time <= selected_time)
                    or (booking_start_time >= timepoint and booking_end_time > timepoint)
                ):
                    blocked_timepoints.append(timepoint)
                    break

        return blocked_timepoints

    async def _render_keyboard(self, data: dict, manager: DialogManager) -> list[list[InlineKeyboardButton]]:
        endpoint_time_selected = self.get_selected_time_points(manager)
        daily_bookings: list[Booking] = data["daily_bookings"]

        if len(endpoint_time_selected) == 0:
            already_booked_timepoints = self.get_already_booked_timepoints(daily_bookings)
            available_timepoints_to_select = self.get_all_time_points()
            blocked_timepoints = self.get_blocked_timepoints(None, daily_bookings)
        elif len(endpoint_time_selected) == 1:
            start_time = endpoint_time_selected[0]
            already_booked_timepoints = self.get_already_booked_timepoints(daily_bookings, reverse=True)
            available_timepoints_to_select = self.get_end_time_points(start_time)
            blocked_timepoints = self.get_blocked_timepoints(start_time, daily_bookings)
        elif len(endpoint_time_selected) == 2:
            already_booked_timepoints = self.get_already_booked_timepoints(daily_bookings, reverse=True)
            available_timepoints_to_select = []
            blocked_timepoints = []
            manager.dialog_data["time_start"] = endpoint_time_selected[0].isoformat()
            manager.dialog_data["time_end"] = endpoint_time_selected[1].isoformat()
        else:
            assert_never(endpoint_time_selected)

        keyboard_builder = InlineKeyboardBuilder()
        for timepoint in self.timepoints:
            time_text = timepoint.strftime("%H:%M")
            time_callback_data = self._item_callback_data(time_text)

            available = timepoint in available_timepoints_to_select
            blocked = timepoint in blocked_timepoints
            already_selected = timepoint in endpoint_time_selected

            if already_selected:
                text = f"{time_text} -" if timepoint == endpoint_time_selected[0] else f"- {time_text}"
                keyboard_builder.button(text=text, callback_data=time_callback_data)
            elif available and not blocked:
                keyboard_builder.button(text=time_text, callback_data=time_callback_data)
            else:
                keyboard_builder.button(text=" ", callback_data=self._item_callback_data("None"))
        
        return keyboard_builder.export()

    def get_selected_time_points(self, manager: DialogManager) -> list[datetime.time]:
        endpoint_time_selected = self.get_widget_data(manager, [])
        return list(map(lambda x: datetime.datetime.strptime(x, "%H:%M").time(), endpoint_time_selected))
    
    async def _process_item_callback(
        self,
        callback: CallbackQuery,
        data: str,
        dialog: DialogProtocol,
        manager: DialogManager,
    ) -> bool:
        """
        Process callback from item
        :param callback: callback
        :param data: callback data
        :param dialog: dialog
        :param manager: dialog manager
        :return: True if processed
        """
        widget_data = self.get_widget_data(manager, [])

        if data == "None":
            if widget_data:
                self.set_widget_data(manager, [])
                return True
            return False
        clicked_timepoint = data
        
        endpoint_timepoints = self.get_widget_data(manager, [])

        if clicked_timepoint in endpoint_timepoints:
            endpoint_timepoints.remove(clicked_timepoint)
        else:
            endpoint_timepoints.append(clicked_timepoint)
        for i in range(len(endpoint_timepoints)):
            if isinstance(endpoint_timepoints[i], datetime.time):
                endpoint_timepoints[i] = endpoint_timepoints[i].isoformat()
        self.set_widget_data(manager, endpoint_timepoints)
        return True
    
    def __init__(
        self,
        timepoints: list[datetime.time],
        id: str,
        when: WhenCondition = None,
    ):
        super().__init__(id=id, when=when)
        self.timepoints = timepoints