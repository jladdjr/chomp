#!/usr/bin/env python3

import argparse
from datetime import datetime
from time import time

from yaml import load, dump, Loader, Dumper

DEFAULT_FOOD_LIBRARY = "/home/jim/git/chomp/food_library.yml"
DEFAULT_FOOD_DIARY = "/home/jim/git/chomp/food_diary.yml"

def get_food_library():
    with open(DEFAULT_FOOD_LIBRARY, 'r') as f:
        data = load(f, Loader)
    return data

def get_food_diary():
    with open(DEFAULT_FOOD_DIARY, 'r') as f:
        data = load(f, Loader=Loader)
    if data is None:
        data = {}
    return data

def write_food_diary(data):
    yaml_diary = dump(data, Dumper=Dumper)
    with open(DEFAULT_FOOD_DIARY, 'w') as f:
        f.write(yaml_diary)

def get_beginning_of_day_timestamp():
    today = datetime.today()
    start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_day.timestamp()

def get_current_time_key():
    return str(int(time()))

def add_food_diary_entry(food, calories):
    """Reads in current food diary and adds a new time-stamped entry that includes:
    - food name (str)
    - calories (int)
    """
    food_diary = get_food_diary()
    time_key = get_current_time_key()
    diary_entry = {'food': food,
                   'calories': calories}
    food_diary[time_key] = diary_entry
    write_food_diary(food_diary)

def eat(args):
    food = args.food

    print(f'You ate {food}')

    food_lib = get_food_library()
    if food in food_lib:
        food_details = food_lib[food]
        if 'cal' in food_details:
            cal = food_details['calories']
            print(f"you ate {cal} calories!")
            add_food_diary_entry(food, cal)
        else:
            print(f"Can't find calorie information for {food}")
    else:
        print("Not found!")

def today(args):
    food_diary = get_food_diary()
    start_of_day = get_beginning_of_day_timestamp()

    calorie_total = 0
    for timestamp in food_diary:
        print(f'found entry for {timestamp}')
        if int(timestamp) < start_of_day:
            print(' before today.. skipping')
            continue
        entry = food_diary[timestamp]
        if 'calories' not in entry:
            print(' missing calorie information.. skipping')
            continue
        calorie_total += entry['calories']
    print(f'Total calories for the day: {calorie_total}')

def main():
    parser = argparse.ArgumentParser(prog='chomp')
    subparsers = parser.add_subparsers(help='sub-command help')

    # eat subparser
    parser_eat = subparsers.add_parser('eat', help='adds a meal to your food diary..')
    parser_eat.add_argument('food', type=str, help='food that you ate')
    parser_eat.set_defaults(func=eat)

    # today subparser
    parser_today = subparsers.add_parser('today', help='get report of food eaten today')
    parser_today.set_defaults(func=today)

    args = parser.parse_args()
    args.func(args)



if __name__ == '__main__':
    main()
