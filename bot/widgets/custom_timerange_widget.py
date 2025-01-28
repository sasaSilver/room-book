import datetime
from typing import TypedDict, assert_never

from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog import DialogManager, DialogProtocol
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Keyboard
from bot.constants import EMOJI_GREEN_CIRCLE, EMOJI_RED_CIRCLE

class Booking(TypedDict):
    id: int
    username: str
    user_full_name: str
    room: str
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time

class TimeRangeWidget(Keyboard):
    """
    Widget for time selection: 07:00, 07:30, 08:00, ...
    """

    def reset(self, manager: DialogManager):
        self.set_widget_data(manager, [])

    def get_start_time_points(self) -> list[datetime.time]:
        return self.timepoints[:-1]
    
    def get_end_time_points(self, start_time: datetime.time) -> list[datetime.time]:
        start_index = self.timepoints.index(start_time)
        return self.timepoints[start_index:]

    def get_already_booked_timepoints(
        self, daily_bookings: list[Booking], reverse: bool = False
    ) -> dict[datetime.time, Booking]:
        already_booked_timepoints: dict[datetime.time, Booking] = {}
        for timeslot in self.timepoints:
            for booking in daily_bookings:
                start_time = booking.start_time
                end_time = booking.end_time

                if not reverse and start_time <= timeslot < end_time:
                    already_booked_timepoints[timeslot] = booking
                    break
                if reverse and start_time < timeslot <= end_time:
                    already_booked_timepoints[timeslot] = booking
                    break
        return already_booked_timepoints

    def get_blocked_timepoints(
        self, selected_time: datetime.time | None, daily_bookings: list[Booking]
    ) -> list[datetime.time]:
        blocked_timepoints = []

        for timepoint in self.timepoints:
            for booking in daily_bookings:
                booking_start_time = booking.start_time
                booking_end_time = booking.end_time
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

    def _get_keyboard_state(self, endpoint_time_selected: list[datetime.time], daily_bookings: list[Booking]) -> tuple[dict[datetime.time, Booking], list[datetime.time], list[datetime.time]]:
        """
        Get the current state of the keyboard based on selected timepoints
        Returns: (already_booked_timepoints, available_timepoints_to_select, blocked_timepoints)
        """
        if len(endpoint_time_selected) == 0:
            return (
                self.get_already_booked_timepoints(daily_bookings),
                self.get_start_time_points(),
                self.get_blocked_timepoints(None, daily_bookings)
            )
        elif len(endpoint_time_selected) == 1:
            start_time = endpoint_time_selected[0]
            return (
                self.get_already_booked_timepoints(daily_bookings, reverse=True),
                self.get_end_time_points(start_time),
                self.get_blocked_timepoints(start_time, daily_bookings)
            )
        elif len(endpoint_time_selected) == 2:
            return (
                self.get_already_booked_timepoints(daily_bookings, reverse=True),
                [],
                []
            )
        else:
            assert_never(endpoint_time_selected)

    def _get_button_text(self, timepoint: datetime.time, endpoint_time_selected: list[datetime.time]) -> str:
        """Generate button text based on timepoint and selection state"""
        time_text = timepoint.strftime("%H:%M")
        if timepoint == endpoint_time_selected[0]:
            return f"{time_text} -"
        elif timepoint == endpoint_time_selected[-1]:
            return f"- {time_text}"
        return time_text

    def _get_filtered_timeslots(self, selected_date: datetime.date) -> list[datetime.time]:
        """Get timeslots filtered by current time if date is today"""
        if selected_date == datetime.datetime.now().date():
            return list(filter(lambda x: datetime.datetime.now().time() <= x, self.timepoints))
        return self.timepoints

    async def _render_keyboard(self, data: dict, manager: DialogManager) -> list[list[InlineKeyboardButton]]:
        """Render the time selection keyboard"""
        # Get selected timepoints and bookings
        endpoint_time_selected = self.get_selected_time_points(manager)
        daily_bookings: list[Booking] = data["daily_bookings"]

        # Get current keyboard state
        already_booked_timepoints, available_timepoints_to_select, blocked_timepoints = self._get_keyboard_state(
            endpoint_time_selected, daily_bookings
        )

        # Store selected times in dialog data if both endpoints are selected
        if not available_timepoints_to_select and not endpoint_time_selected:
            return []
        if len(endpoint_time_selected) == 2:
            manager.dialog_data["start_time"] = endpoint_time_selected[0].isoformat()
            manager.dialog_data["end_time"] = endpoint_time_selected[1].isoformat()

        keyboard_builder = InlineKeyboardBuilder()
        
        selected_date = manager.dialog_data["selected_date"]
        timeslots = self._get_filtered_timeslots(selected_date)
        
        if len(timeslots) == 1 and len(endpoint_time_selected) == 0:
            return 
        
        # Build keyboard buttons
        for timepoint in timeslots:
            time_callback_data = self._item_callback_data(timepoint.strftime("%H:%M"))

            # Determine button state
            available = timepoint in available_timepoints_to_select
            blocked = timepoint in blocked_timepoints
            already_selected = timepoint in endpoint_time_selected
            booked_by_someone = timepoint in already_booked_timepoints

            # Render appropriate button based on state
            if already_selected:
                text = self._get_button_text(timepoint, endpoint_time_selected)
                keyboard_builder.button(text=text, callback_data=time_callback_data)
            elif available and not blocked:
                keyboard_builder.button(
                    text=timepoint.strftime("%H:%M"),
                    callback_data=time_callback_data
                )
            elif booked_by_someone:
                booking = already_booked_timepoints[timepoint]
                if booking.username == manager.event.from_user.username:
                    keyboard_builder.button(
                        text=EMOJI_GREEN_CIRCLE,
                        callback_data=self._item_callback_data("None")
                    )
                else:
                    keyboard_builder.button(
                        text=EMOJI_RED_CIRCLE,
                        url=f"https://t.me/{booking.username}"
                    )
            else:
                keyboard_builder.button(
                    text=" ",
                    callback_data=self._item_callback_data("None"),
                )

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