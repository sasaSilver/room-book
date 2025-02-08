from PIL import Image, ImageDraw, ImageFont
import datetime, io

# Configuration (all dimensions multiplied by 4)
TIME_START = 0
TIME_END = 10
TIME_COLUMN_WIDTH = 70 * 4
ROOM_HEADER_HEIGHT = 48 * 4
HOUR_HEIGHT = 60 * 4
BOOKING_PADDING = 4 * 4
DATE_HEADER_HEIGHT = 40 * 4
CORNER_RADIUS = 7 * 4

# Calculate dimensions
TOTAL_WIDTH = 400 * 4
TOTAL_HEIGHT = DATE_HEADER_HEIGHT + ROOM_HEADER_HEIGHT + (TIME_END - TIME_START) * HOUR_HEIGHT

COLORS = {
    'background': '#FFFFFF',
    'grid_lines': '#E9ECEF',
    'time_text': '#6C757D',
    'room_colors': ['#D0E6A5', '#FFDDC1', '#A5D8FF', '#FFC9C9'],
    'now_line': '#FF0053'
}

def get_bookings_img_bytes(date, rooms, bookings):
    
    # Create image
    img = Image.new('RGB', (TOTAL_WIDTH, TOTAL_HEIGHT), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        font_bold = ImageFont.truetype("arialbd.ttf", 16 * 4)
        font_medium = ImageFont.truetype("arial.ttf", 14 * 4)
        font_bmedium = ImageFont.truetype("arialbd.ttf", 14 * 4)
        font_regular = ImageFont.truetype("arial.ttf", 12 * 4)
        font_bregular = ImageFont.truetype("arialbd.ttf", 12 * 4)
    except:
        font_bold = ImageFont.load_default(16 * 4)
        font_medium = ImageFont.load_default(14 * 4)
        font_bmedium = ImageFont.load_default(14 * 4)
        font_regular = ImageFont.load_default(12 * 4)
        font_bregular = ImageFont.load_default(12 * 4)

    
    now = datetime.datetime.now()
    
    # "Now time" hline
    if date == now.date():
        now_minutes = now.hour * 60 + now.minute
        minute_height = HOUR_HEIGHT / 60
        now_y = ROOM_HEADER_HEIGHT + minute_height * now_minutes
        line_start = (TIME_COLUMN_WIDTH, now_y)
        line_end = (TOTAL_WIDTH, now_y)

        # Draw the line
        draw.line([line_start, line_end], fill=COLORS['now_line'], width=3)

        # Circle at the start of the line
        circle_radius = 10 
        circle_center = (line_start[0], line_start[1])
        circle_bbox = [
            circle_center[0] - circle_radius,
            circle_center[1] - circle_radius,
            circle_center[0] + circle_radius,
            circle_center[1] + circle_radius
        ]
        draw.ellipse(circle_bbox, outline=COLORS['now_line'], width=3, fill=COLORS['now_line'])
    
    # Draw date in the top-left corner
    date_text = date.strftime('%b %d')  # "Feb 25"
    day_text = date.strftime('%a')      # "Fri"
    
    draw.text((10 * 4, 10 * 4), date_text, font=font_bold, fill='#2B2D42')
    draw.text((10 * 4, 30 * 4), day_text, font=font_medium, fill='#6C757D')

    # Draw room headers at the top
    room_width = (TOTAL_WIDTH - TIME_COLUMN_WIDTH) / len(rooms)
    for idx, room in enumerate(rooms):
        x_start = TIME_COLUMN_WIDTH + idx * room_width
        color = COLORS['room_colors'][idx % len(COLORS['room_colors'])]
        
        # Draw room header
        rectangle_offset = 5 * 4
        draw.rounded_rectangle(
            [
                (x_start + rectangle_offset, 0 + rectangle_offset),
                (x_start + room_width - rectangle_offset, ROOM_HEADER_HEIGHT - rectangle_offset)
            ],
            radius=CORNER_RADIUS,
            fill=color
        )
        draw.text(
            (x_start + room_width/2, ROOM_HEADER_HEIGHT/2),
            room,
            font=font_bmedium,
            fill='#2B2D42',
            anchor='mm'
        )

    # Draw timeline
    for hour in range(TIME_START, TIME_END + 1):
        y = ROOM_HEADER_HEIGHT + (hour - TIME_START) * HOUR_HEIGHT
        draw.line([(0, y), (TOTAL_WIDTH, y)], fill=COLORS['grid_lines'], width=3)
        draw.text(
            (5 * 4, y + 5 * 4),
            f"{hour:02d}:00",
            font=font_bregular,
            fill=COLORS['time_text']
        )

    # Draw bookings
    for room_idx, room in enumerate(rooms):
        room_x_start = TIME_COLUMN_WIDTH + room_idx * room_width
        color = COLORS['room_colors'][room_idx % len(COLORS['room_colors'])]
        
        for booking in bookings[room]:
            if booking.date != date:
                continue
                
            start_h = booking.start_time.hour + booking.start_time.minute/60
            end_h = booking.end_time.hour + booking.end_time.minute/60
            
            y_start = ROOM_HEADER_HEIGHT + (start_h - TIME_START) * HOUR_HEIGHT
            y_end = ROOM_HEADER_HEIGHT + (end_h - TIME_START) * HOUR_HEIGHT
            
            # Draw booking block
            draw.rounded_rectangle(
                [
                    (room_x_start + BOOKING_PADDING, y_start + BOOKING_PADDING),
                    (room_x_start + room_width - BOOKING_PADDING, y_end - BOOKING_PADDING)
                ],
                radius=CORNER_RADIUS,
                fill=color,
                outline='#FFFFFF',
                width=2 * 4
            )

            # Format booking text
            time_str = f"{booking.start_time.strftime('%H:%M')}-{booking.end_time.strftime('%H:%M')}"
            user_lines = _wrap_text(booking.user_full_name, room_width - 20 * 4, font_regular, draw)
            
            # Draw text
            text_y = y_start + 8 * 4
            draw.text(
                (room_x_start + 8 * 4, text_y),
                time_str,
                font=font_regular,
                fill='#495057',
            )
            for line in user_lines:
                text_y += 14 * 4
                draw.text(
                    (room_x_start + 8 * 4, text_y),
                    line,
                    font=font_regular,
                    fill='#212529'
                )
                
    img_bytes_buffer = io.BytesIO()
    img.save(img_bytes_buffer, format='PNG')
    img_bytes = img_bytes_buffer.getvalue()
    img.close()
    
    return img_bytes

def _wrap_text(text, max_width, font, draw):
    words = text.split('_')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if draw.textlength(test_line, font=font) < max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

if __name__ == "__main__":
    import bot.database.db_op as db_op
    from bot.settings import settings
    import asyncio
    
    # Test data generation
    async def create_test_data():
        today = datetime.date.today() # This is a Sunday
        data =  {
            "date": today,
            "rooms": settings.rooms,
            "bookings": {}
        }
        for room in settings.rooms:
            data["bookings"][room] = await db_op.get_bookings_by_room(room)
        return data
        
    
    test_data = asyncio.run(create_test_data())
    img_bytes = get_bookings_img_bytes(test_data['date'], test_data['rooms'], test_data['bookings'])
    
    # Save the image to a file
    with open('schedule.png', 'wb') as f:
        f.write(img_bytes)
    