import datetime
import io
from typing import List

from PIL import Image, ImageDraw, ImageFont

from bot.database.schemas import BookingSchema
from bot.settings import settings
from bot.utils.utils import to_timeslot_str

# Configuration (all dimensions multiplied by 4)
TIME_START = settings.start_time.hour
TIME_END = settings.end_time.hour + 1  # + 1 for extra space below
TIME_COLUMN_WIDTH = 70 * 4
ROOM_HEADER_HEIGHT = 48 * 4
HOUR_HEIGHT = 60 * 4
BOOKING_PADDING = 4 * 4
DATE_HEADER_HEIGHT = 40 * 4
CORNER_RADIUS = 7 * 4

# Image dimensions
TOTAL_WIDTH = 500 * 4
TOTAL_HEIGHT = (
    DATE_HEADER_HEIGHT + ROOM_HEADER_HEIGHT + (TIME_END - TIME_START) * HOUR_HEIGHT
)

COLORS = {
    "background": "#FFFFFF",
    "grid_lines": "#E9ECEF",
    "time_text": "#6C757D",
    "room_colors": ["#D0E6A5", "#FFDDC1", "#A5D8FF", "#FFC9C9"],
    "now_line": "#FF0053",
    "room_header": "#2B2D42",
    "date_text": "#2B2D42",
    "day_text": "#6C757D"
}


def get_bookings_img_bytes(
    date: datetime.date, rooms: List[str], bookings: List[BookingSchema]
):

    # Create image
    img = Image.new("RGB", (TOTAL_WIDTH, TOTAL_HEIGHT), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    # Load fonts
    try:
        font_bold = ImageFont.truetype("arialbd.ttf", 16 * 4)
        font_medium = ImageFont.truetype("arial.ttf", 14 * 4)
        font_bmedium = ImageFont.truetype("arialbd.ttf", 14 * 4)
        font_regular = ImageFont.truetype("arial.ttf", 12 * 4)
        font_bregular = ImageFont.truetype("arialbd.ttf", 12 * 4)
    except OSError:
        font_bold = ImageFont.load_default(16 * 4)
        font_medium = ImageFont.load_default(14 * 4)
        font_bmedium = ImageFont.load_default(14 * 4)
        font_regular = ImageFont.load_default(12 * 4)
        font_bregular = ImageFont.load_default(12 * 4)

    now = datetime.datetime.now()

    # Red line indicating curr time
    if date == now.date():
        now_minutes = now.hour * 60 + now.minute
        minute_height = HOUR_HEIGHT / 60
        now_y = ROOM_HEADER_HEIGHT + minute_height * now_minutes
        line_start = (TIME_COLUMN_WIDTH, now_y)
        line_end = (TOTAL_WIDTH, now_y)

        # Draw the line
        draw.line([line_start, line_end], fill=COLORS["now_line"], width=3)

        # Circle at the start of the line
        circle_radius = 15
        circle_center = (line_start[0], line_start[1])
        circle_bbox = [
            circle_center[0] - circle_radius,
            circle_center[1] - circle_radius,
            circle_center[0] + circle_radius,
            circle_center[1] + circle_radius,
        ]
        draw.ellipse(circle_bbox, width=3, fill=COLORS["now_line"])

    # Draw date in the top-left corner
    date_text = f"{date.strftime("%b").capitalize()} {date.strftime("%d")}" # Фев 19
    day_text = date.strftime("%a")  # "Fri"

    draw.text((10 * 4, 10 * 4), date_text, font=font_bold, fill=COLORS["date_text"])
    draw.text((10 * 4, 30 * 4), day_text, font=font_medium, fill=COLORS["day_text"])

    # Draw room headers at the top
    room_width = (TOTAL_WIDTH - TIME_COLUMN_WIDTH) / len(rooms)
    for idx, room in enumerate(rooms):
        x_start = TIME_COLUMN_WIDTH + idx * room_width
        color = COLORS["room_colors"][idx % len(COLORS["room_colors"])]

        # Draw room header
        rectangle_offset = 5 * 4
        draw.rounded_rectangle(
            [
                (x_start + rectangle_offset, 0 + rectangle_offset),
                (
                    x_start + room_width - rectangle_offset,
                    ROOM_HEADER_HEIGHT - rectangle_offset,
                ),
            ],
            radius=CORNER_RADIUS,
            fill=color,
        )
        draw.text(
            (x_start + room_width / 2, ROOM_HEADER_HEIGHT / 2),
            room,
            font=font_bmedium,
            fill=COLORS["room_header"],
            anchor="mm",
        )

    # Draw timeline
    for hour in range(TIME_START, TIME_END + 1):
        y = ROOM_HEADER_HEIGHT + (hour - TIME_START) * HOUR_HEIGHT
        draw.line([(0, y), (TOTAL_WIDTH, y)], fill=COLORS["grid_lines"], width=3)
        draw.text(
            (5 * 4, y + 5 * 4),
            f"{hour:02d}:00",
            font=font_bregular,
            fill=COLORS["time_text"],
        )

    # Draw bookings
    for room_idx, room in enumerate(rooms):
        room_x_start = TIME_COLUMN_WIDTH + room_idx * room_width
        color = COLORS["room_colors"][room_idx % len(COLORS["room_colors"])]

        for booking in bookings:
            if booking.date != date or booking.room != room:
                continue

            start_h = booking.start_time.hour + booking.start_time.minute / 60
            end_h = booking.end_time.hour + booking.end_time.minute / 60

            y_start = ROOM_HEADER_HEIGHT + (start_h - TIME_START) * HOUR_HEIGHT
            y_end = ROOM_HEADER_HEIGHT + (end_h - TIME_START) * HOUR_HEIGHT

            # Draw booking block
            draw.rounded_rectangle(
                [
                    (room_x_start + BOOKING_PADDING, y_start + BOOKING_PADDING),
                    (
                        room_x_start + room_width - BOOKING_PADDING,
                        y_end - BOOKING_PADDING,
                    ),
                ],
                radius=CORNER_RADIUS,
                fill=color,
                outline="#FFFFFF",
                width=2 * 4,
            )

            # Format booking text
            name = _insert_newlines(booking.user_full_name, 18)
            draw.multiline_text(
                (room_x_start + 8 * 4, y_start + 19 * 4),
                name,
                fill="#212529",
                font=font_regular,
            )
            # Draw text
            text_y = y_start + 8 * 4
            time_str = to_timeslot_str(booking.start_time, booking.end_time)
            draw.text(
                (room_x_start + 8 * 4, text_y),
                time_str,
                font=font_regular,
                fill="#495057",
            )

    img_bytes_buffer = io.BytesIO()
    img.save(img_bytes_buffer, format="JPEG")
    schedule_bytes = img_bytes_buffer.getvalue()
    img.close()
    return schedule_bytes


def _insert_newlines(text, max_length):
    return "\n".join(
        text[i: i + max_length] for i in range(0, len(text), max_length)
    )


if __name__ == "__main__":
    import bot.database.db_op as db_op
    import asyncio

    # Test data generation
    async def create_test_data():
        today = datetime.date.today()
        data = {
            "date": today,
            "rooms": settings.rooms,
            "bookings": await db_op.get_all_bookings(),
        }
        return data

    test_data = asyncio.run(create_test_data())
    img_bytes = get_bookings_img_bytes(
        test_data["date"], test_data["rooms"], test_data["bookings"]
    )

    # Save the image to a file
    with open("schedule.jpeg", "wb") as f:
        f.write(img_bytes)
