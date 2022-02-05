#!/usr/bin/env python3

import argparse
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


def main():
    parser = argparse.ArgumentParser(prog='chomp')
    subparsers = parser.add_subparsers(help='eat command adds a meal to your food diary')
    parser_eat = subparsers.add_parser('eat', help='eat command adds a meal to your food diary..')
    parser_eat.add_argument('food', type=str, help='food that you ate')
    args = parser.parse_args()

    food = args.food

    print(f'You ate {food}')

    food_lib = get_food_library()
    if food in food_lib:
        food_details = food_lib[food]
        if 'cal' in food_details:
            cal = food_details['cal']
            print(f"you ate {cal} calories!")
            add_food_diary_entry(food, cal)
        else:
            print(f"Can't find calorie information for {food}")
    else:
        print("Not found!")


if __name__ == '__main__':
    main()
