#!/usr/bin/env python3

import argparse

from chomp.commands import eat, cook, today, weight, lookup_food


def main():
    parser = argparse.ArgumentParser(prog="chomp")
    subparsers = parser.add_subparsers(help="sub-command help")

    # eat subparser
    parser_eat = subparsers.add_parser("eat", help="adds a meal to your food diary..")
    parser_eat.add_argument("food", type=str, help="food that you ate")
    parser_eat.add_argument(
        "--percent",
        type=float,
        default=1.0,
        help="(optional) specify portion (where 1.0 is a std portion)",
    )
    parser_eat.add_argument(
        "--weight", type=float, default=None, help="(optional) specify weight"
    )
    parser_eat.set_defaults(func=eat)

    # cook subparser
    parser_cook = subparsers.add_parser("cook", help="adds an ingredient to a recipe (starting a new recipe if needed)")
    parser_cook.add_argument("recipe", type=str, help="name of recipe")
    parser_cook.add_argument("ingredient", type=str, help="ingredient name (must exist in food library)")
    parser_cook.add_argument(
        "--percent",
        type=float,
        default=1.0,
        help="(optional) specify portion of ingredient (where 1.0 is a std portion)",
    )
    parser_cook.add_argument(
        "--weight", type=float, default=None, help="(optional) specify weight of ingredient"
    )
    parser_cook.set_defaults(func=cook)

    # today subparser
    parser_today = subparsers.add_parser("today", help="get report of food eaten today")
    parser_today.set_defaults(func=today)

    # weight subparser
    parser_weight = subparsers.add_parser("weight", help="add today's weight")
    parser_weight.add_argument("weight", type=float, help="today's weight")
    parser_weight.set_defaults(func=weight)

    # food lookup subparser
    parser_food_lookup = subparsers.add_parser(
        "list_foods", help="get list of foods matching name or description"
    )
    parser_food_lookup.add_argument(
        "food", type=str, help="name or description of food"
    )
    parser_food_lookup.set_defaults(func=lookup_food)

    args = parser.parse_args()
    if "func" not in args:
        parser.print_help()
    else:
        # TODO: There's got to be a better way to map arguments received to the command functions
        if args.func == eat:
            eat(args.food, args.weight, args.percent)
        elif args.func == today:
            today()
        elif args.func == weight:
            weight(args.weight)
        elif args.func == lookup_food:
            lookup_food(args.food)
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
