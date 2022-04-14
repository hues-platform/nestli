def get_seconds_from_date(day: int, month: int) -> int:
    days = 0
    for i in range(month - 1):
        days += days_in_month[i]
    seconds = (days + day - 1) * 3600 * 24
    return (seconds)


days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
