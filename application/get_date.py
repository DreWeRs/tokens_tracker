from datetime import date


def get_date() -> tuple[int, int, int]:
    current_date = date.today()
    return current_date.year, current_date.month, current_date.day
