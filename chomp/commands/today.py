from copy import copy
from datetime import datetime

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
    combined_intake = {}
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
        food = entry["food"]
        name = food.name
        calories = food.get_nutritional_fact('calories')
        fat = food.get_nutritional_fact('fat') or 0
        info_line = f"{time_of_day}    {name:39}   {calories:13}   {fat:^7}"
        print(info_line)

        # TODO: Add support for summing food nutritional data
        combined_intake = _merge_nutritional_facts(combined_intake, consumed)
    print()
    print(f"Total calories for the day: {combined_intake['calories']}")

def _merge_nutritional_facts(first_fact_set, second_fact_set):
    # copy all entries from first_fact_set except nested dictionaries
    combined_facts = {k:v for (k,v) in first_fact_set.items() if type(k) is not dict}

    # merge in entries from second_fact_set, ignoring nested dictionaries
    for key, value in second_fact_set.items():
        if type(value) is dict:
            continue

        if key not in combined_facts:
            combined_facts[key] = value
        else:
            combined_facts[key] += value

    # handle nested dictionaries
    for key, value in first_fact_set.items():
        if type(value) is not dict:
            continue
        # determine if merge is required
        if key in second_fact_set:
            other_value = second_fact_set[key]
            combined_facts[key] = _merge_nutritional_facts(value, other_value)
        else:
            combined_facts[key] = value

    for key, value in second_fact_set.items():
        if type(value) is not dict:
            continue
        # at this point, only need to handle cases where
        # key is not in first_fact_set
        if key not in first_fact_set:
            combined_facts[key] = value
            
    return combined_facts
