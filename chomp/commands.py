from datetime import datetime

import openfoodfacts

from chomp.data_manager import (
    add_food_diary_entry,
    get_food,
    get_food_diary,
    add_weight_diary_entry,
    FoodNotFoundException,
)
from chomp.utils import get_beginning_of_day_timestamp


def eat(food_name, weight=None, percent=1):
    if abs(percent - 1) < 0.001:
        print(f"You ate {food_name}")
    else:
        print(f"You ate {100 * percent:.1f}% of {food_name}")

    try:
        food_details = get_food(food_name)
        if "calories" in food_details:
            if weight:
                food_weight = food_details["weight"]
                percent = weight / food_weight
            cal = int(food_details["calories"] * percent)
            print(f"You ate {cal} calories!")
            add_food_diary_entry(food_name, cal)
        else:
            print(f"Can't find calorie information for {food_name}")
    except FoodNotFoundException:
        print(f"Cannot find {food_name}!")


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
        if "calories" not in entry:
            print(" missing calorie information.. skipping")
            continue

        time_of_day = datetime.fromtimestamp(int(timestamp))
        calories = entry["calories"]
        food = entry["food"]
        info_line = f"{time_of_day}    {food:39}   {calories:^7}"
        print(info_line)

        calorie_total += entry["calories"]
    print()
    print(f"Total calories for the day: {calorie_total}")


def weight(weight):
    print(f"You weigh {weight} pounds!")
    add_weight_diary_entry(weight)


def lookup_food(food):
    search_results = openfoodfacts.products.search(food)
    products = search_results["products"]

    product_search_normalized = {}
    max_product_length = 1
    max_generic_length = 1
    for i, prod in enumerate(products):
        product_name = prod.get("product_name", "").strip()
        generic_name = prod.get("generic_name", "").strip()
        if len(product_name) > max_product_length:
            max_product_length = len(product_name)
        if len(generic_name) > max_generic_length:
            max_generic_length = len(generic_name)

        product_search_normalized[i] = {
            "generic_name": generic_name,
            "product_name": product_name,
        }

    print("Results")
    for index, prod in product_search_normalized.items():
        info_line = f"{index:3}    {prod['product_name']:{max_product_length}}   {prod['generic_name']:{max_generic_length}}"
        print(info_line)
