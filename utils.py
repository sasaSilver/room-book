import datetime

def generate_timeslots(start_time: datetime.time, end_time: datetime.time, interval: int) -> list[datetime.time]:
    timeslots = []
    current_time = start_time
    while current_time <= end_time:
        timeslots.append(current_time)
        current_time = (
            datetime.datetime.combine(datetime.datetime.today(), current_time) + datetime.timedelta(minutes=interval)
        ).time()
    return timeslots