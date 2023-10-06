from copy import copy
from datetime import datetime

from tabulate import tabulate

from chomp.food import Food
from chomp.data_manager import (
    get_food_diary,
)
from chomp.utils import get_beginning_of_day_timestamp


def today():
    food_diary = get_food_diary()
    start_of_day = get_beginning_of_day_timestamp()

    lines = [['Time of Day', 'Food', 'Calories', 'Fat']]

    combined_intake = None
    for timestamp in food_diary:
        if int(timestamp) < start_of_day:
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
        lines.append([time_of_day, name, calories, fat])

        if combined_intake is None:
            combined_intake = food
        else:
            combined_intake += food
    print(tabulate(lines, headers="firstrow", tablefmt="rounded_outline"))

    print()

    lines = [['Total Calories', 'Total Fat']]
    lines.append([combined_intake.get_nutritional_fact('calories'),
                  combined_intake.get_nutritional_fact('fat.total')])
    print(tabulate(lines, headers="firstrow", tablefmt="rounded_outline"))
