def get_seconds_from_date(day: int, month: int):
    seconds = 0
    for i in range(month-1):
        seconds += days_in_month[i] * 3600 * 24
    seconds += (day-1) * 3600 * 24
    return seconds

days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]