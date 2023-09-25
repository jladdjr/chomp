from datetime import datetime

from chomp.data_manager import (
    get_food_diary,
)
from chomp.utils import get_beginning_of_day_timestamp


def today():
    food_diary = get_food_diary()
    start_of_day = get_beginning_of_day_timestamp()

    print(
        f"      time_of_day    |                   food               |    calories  "
    )
    print(
        f"---------------------------------------------------------------------------"
    )
    calorie_total = 0
    for timestamp in food_diary:
        # print(f'found entry for {timestamp}')
        if int(timestamp) < start_of_day:
            # print(' before today.. skipping')
            continue
        entry = food_diary[timestamp]
        if "consumed" not in entry:
            print(" missing food diary data for entry.. skipping")
            continue

        time_of_day = datetime.fromtimestamp(int(timestamp))
        consumed = entry["consumed"]
        food = entry["food"]
        info_line = f"{time_of_day}    {food:39}   {consumed['calories']:^7}"
        print(info_line)

        calorie_total += consumed["calories"]
    print()
    print(f"Total calories for the day: {calorie_total}")
