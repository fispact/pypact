
SECS_IN_HOUR = 60 * 60
SECS_IN_DAY = 24 * SECS_IN_HOUR
SECS_IN_WEEK = 7 * SECS_IN_DAY
SECS_IN_MONTH = 30 * SECS_IN_DAY
SECS_IN_YEAR = 365.25 * SECS_IN_DAY
SECS_IN_DECADE = 10 * SECS_IN_YEAR
SECS_IN_MILLENIUM = 100 * SECS_IN_DECADE


def get_time_string(time):
    # very dumb code...
    if time < SECS_IN_HOUR:
        return f"{time:.1f} s"
    if time < SECS_IN_DAY:
        return f"{time/SECS_IN_HOUR:.1f} hour"
    if time < SECS_IN_WEEK:
        return f"{time/SECS_IN_DAY:.1f} day"
    if time < SECS_IN_MONTH:
        return f"{time/SECS_IN_WEEK:.1f} week"
    if time < SECS_IN_YEAR:
        return f"{time/SECS_IN_MONTH:.1f} month"
    if time < SECS_IN_DECADE:
        return f"{time/SECS_IN_YEAR:.1f} year"
    if time < SECS_IN_MILLENIUM:
        return f"{time/SECS_IN_DECADE:.1f} decade"
    return f"{time/SECS_IN_DECADE:.1f} millennia"