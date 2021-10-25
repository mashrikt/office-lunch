from datetime import datetime, timedelta


def get_last_n_working_days(n):
    last_working_days = []
    delta = 1
    today = datetime.today().date()

    while len(last_working_days) < n:
        day = today - timedelta(days=delta)
        delta += 1
        if day.weekday() < 5:
            last_working_days.append(day)
    return last_working_days
