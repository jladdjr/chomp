#!/usr/bin/env python3

import argparse
from datetime import datetime
from time import time

from yaml import load, dump, Loader, Dumper

DEFAULT_FOOD_LIBRARY = "/home/jim/.chomp/food_library.yml"
DEFAULT_FOOD_DIARY = "/home/jim/.chomp/food_diary.yml"
DEFAULT_WEIGHT_DIARY = "/home/jim/.chomp/weight_diary.yml"

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

def get_weight_diary():
    with open(DEFAULT_WEIGHT_DIARY, 'r') as f:
        data = load(f, Loader=Loader)
    if data is None:
        data = {}
    return data

def write_weight_diary(data):
    yaml_diary = dump(data, Dumper=Dumper)
    with open(DEFAULT_WEIGHT_DIARY, 'w') as f:
        f.write(yaml_diary)

def add_weight_diary_entry(weight):
    weight_diary = get_weight_diary()

    time_key = get_current_time_key()
    diary_entry = {'weight': weight}
    weight_diary[time_key] = diary_entry
    write_weight_diary(weight_diary)

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
    percent = args.percent
    weight = args.weight

    if abs(percent - 1) < 0.001:
        print(f'You ate {food}')
    else:
        print(f'You ate {100 * percent:.1f}% of {food}')

    food_lib = get_food_library()
    if food in food_lib:
        food_details = food_lib[food]
        if 'calories' in food_details:
            if weight:
                food_weight = food_lib[food]['weight']
                percent = weight / food_weight
            cal = int(food_details['calories'] * percent)
            print(f"you ate {cal} calories!")
            add_food_diary_entry(food, cal)
        else:
            print(f"Can't find calorie information for {food}")
    else:
        print("Not found!")

def today(args):
    food_diary = get_food_diary()
    start_of_day = get_beginning_of_day_timestamp()

    print(f'      time_of_day    |                   food               |    calories  ')
    print(f'---------------------------------------------------------------------------')
    calorie_total = 0
    for timestamp in food_diary:
        #print(f'found entry for {timestamp}')
        if int(timestamp) < start_of_day:
            #print(' before today.. skipping')
            continue
        entry = food_diary[timestamp]
        if 'calories' not in entry:
            print(' missing calorie information.. skipping')
            continue

        time_of_day = datetime.fromtimestamp(int(timestamp))
        calories = entry['calories']
        food = entry['food']
        info_line = f'{time_of_day}    {food:39}   {calories:^7}'
        print(info_line)

        calorie_total += entry['calories']
    print()
    print(f'Total calories for the day: {calorie_total}')

def weight(args):
    weight = args.weight
    print(f"You weigh {weight} pounds!")
    add_weight_diary_entry(weight)

def main():
    parser = argparse.ArgumentParser(prog='chomp')
    subparsers = parser.add_subparsers(help='sub-command help')

    # eat subparser
    parser_eat = subparsers.add_parser('eat', help='adds a meal to your food diary..')
    parser_eat.add_argument('food', type=str, help='food that you ate')
    parser_eat.add_argument('--percent', type=float, default=1.0,
                            help='(optional) specify portion (where 1.0 is a std portion)')
    parser_eat.add_argument('--weight', type=float, default=None,
                            help='(optional) specify weight')
    parser_eat.set_defaults(func=eat)

    # today subparser
    parser_today = subparsers.add_parser('today', help='get report of food eaten today')
    parser_today.set_defaults(func=today)

    # weight subparser
    parser_weight = subparsers.add_parser('weight', help="add today's weight")
    parser_weight.add_argument('weight', type=float, help="today's weight")
    parser_weight.set_defaults(func=weight)

    args = parser.parse_args()
    if 'func' not in args:
        parser.print_help()
    else:
        args.func(args)

if __name__ == '__main__':
    main()
