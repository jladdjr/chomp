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

    lines = [['Time of Day', 'Food', 'Calories', 'Fat', 'Protein', 'Carbs']]

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
        calories = round(food.get_nutritional_fact('calories'))
        fat = round(food.get_nutritional_fact('fat.total') or 0)
        protein = round(food.get_nutritional_fact('protein') or 0)
        carbs = round(food.get_nutritional_fact('carbohydrates.total') or 0)
        lines.append([time_of_day, name, calories, fat, protein, carbs])

        if combined_intake is None:
            combined_intake = food
        else:
            combined_intake += food
    print(tabulate(lines, headers="firstrow", tablefmt="rounded_outline"))

    print()

    lines = [['Total Calories', 'Total Fat', 'Total Protein', 'Total Carbs']]
    lines.append([round(combined_intake.get_nutritional_fact('calories')),
                  round(combined_intake.get_nutritional_fact('fat.total')),
                  round(combined_intake.get_nutritional_fact('protein')),
                  round(combined_intake.get_nutritional_fact('carbohydrates.total'))])
    print(tabulate(lines, headers="firstrow", tablefmt="rounded_outline"))

    lines = [['Daily Calories', 'Daily Fat', 'Daily Protein', 'Daily Carbs'],
             [3058, '68 - 119g', 73, '344 - 497g']]
    print(tabulate(lines, headers="firstrow", tablefmt="rounded_outline"))
