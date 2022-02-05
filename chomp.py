#!/usr/bin/env python3

import argparse

def main():
    parser = argparse.ArgumentParser(prog='chomp')
    subparsers = parser.add_subparsers(help='eat command adds a meal to your food diary')
    parser_eat = subparsers.add_parser('eat', help='eat command adds a meal to your food diary..')
    parser_eat.add_argument('food', type=str, help='food that you ate')
    args = parser.parse_args()

    print(f'You ate {args.food}')

if __name__ == '__main__':
    main()
