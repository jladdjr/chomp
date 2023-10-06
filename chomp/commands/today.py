from copy import copy
from datetime import datetime

from chomp.food import Food
from chomp.data_manager import (
    get_food_diary,
)
from chomp.utils import get_beginning_of_day_timestamp


def today():
    food_diary = get_food_diary()
    start_of_day = get_beginning_of_day_timestamp()

    print(
        f"      time_of_day    |                   food               |    calories  |    fat"
    )
    print(
        f"----------------------------------------------------------------------------------------"
    )
    combined_intake = None
    for timestamp in food_diary:
        # print(f'found entry for {timestamp}')
        if int(timestamp) < start_of_day:
            # print(' before today.. skipping')
            continue
        entry = food_diary[timestamp]
        if "food" not in entry:
            print(" missing food diary data for entry.. skipping")
            continue

        time_of_day = datetime.fromtimestamp(int(timestamp))
        food = Food.from_dict(entry["food"])
        name = food.name
        calories = food.get_nutritional_fact('calories')
        fat = food.get_nutritional_fact('fat.total') or 0
        info_line = f"{time_of_day}    {name:39}   {calories:13}   {fat:^7}"
        print(info_line)

        if combined_intake is None:
            combined_intake = food
        else:
            combined_intake += food
    print()
    print(f"Total calories for the day: {combined_intake.get_nutritional_fact('calories')}")

