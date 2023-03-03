from datetime import datetime
from time import time


def get_beginning_of_day_timestamp():
    today = datetime.today()
    start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_day.timestamp()


def get_current_time_key():
    return str(int(time()))
