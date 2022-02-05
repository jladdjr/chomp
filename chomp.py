#!/usr/bin/env python3

import argparse

from yaml import load, dump, Loader, Dumper

DEFAULT_FOOD_LIBRARY = "food_library.yml"

def get_food_library():
    with open(DEFAULT_FOOD_LIBRARY, 'r') as f:
        data = load(f, Loader)
    return data

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
            print(f"you ate {food_details['cal']} calories!")
        else:
            print(f"Can't find calorie information for {food}")
    else:
        print("Not found!")


if __name__ == '__main__':
    main()
