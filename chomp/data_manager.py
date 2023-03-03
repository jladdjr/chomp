from yaml import load, dump, Loader, Dumper

from chomp.utils import get_current_time_key

DEFAULT_FOOD_LIBRARY = "/home/jim/.chomp/food_library.yml"
DEFAULT_FOOD_DIARY = "/home/jim/.chomp/food_diary.yml"
DEFAULT_WEIGHT_DIARY = "/home/jim/.chomp/weight_diary.yml"

# food library


def get_food_library():
    with open(DEFAULT_FOOD_LIBRARY, "r") as f:
        data = load(f, Loader)
    return data


class FoodNotFoundException(Exception):
    pass


def get_food(name):
    food_lib = get_food_library()
    if food in food_lib:
        return food_lib[food]
    raise FoodNotFoundException


# food diary


def add_food_diary_entry(food, calories):
    """Reads in current food diary and adds a new time-stamped entry that includes:
    - food name (str)
    - calories (int)
    """
    food_diary = get_food_diary()
    time_key = get_current_time_key()
    diary_entry = {"food": food, "calories": calories}
    food_diary[time_key] = diary_entry
    write_food_diary(food_diary)


def get_food_diary():
    with open(DEFAULT_FOOD_DIARY, "r") as f:
        data = load(f, Loader=Loader)
    if data is None:
        data = {}
    return data


def write_food_diary(data):
    yaml_diary = dump(data, Dumper=Dumper)
    with open(DEFAULT_FOOD_DIARY, "w") as f:
        f.write(yaml_diary)


# weight diary


def add_weight_diary_entry(weight):
    weight_diary = get_weight_diary()

    time_key = get_current_time_key()
    diary_entry = {"weight": weight}
    weight_diary[time_key] = diary_entry
    write_weight_diary(weight_diary)


def get_weight_diary():
    with open(DEFAULT_WEIGHT_DIARY, "r") as f:
        data = load(f, Loader=Loader)
    if data is None:
        data = {}
    return data


def write_weight_diary(data):
    yaml_diary = dump(data, Dumper=Dumper)
    with open(DEFAULT_WEIGHT_DIARY, "w") as f:
        f.write(yaml_diary)
