from chomp.data_manager import (
    add_food_diary_entry,
    get_food,
    FoodNotFoundException,
)


def eat(food_name, calories=None, weight=None, percent=1):
    if abs(percent - 1) < 0.001:
        print(f"You ate {food_name}")
    else:
        print(f"You ate {100 * percent:.1f}% of {food_name}")

    # if calories are provided, no need to look up food
    if calories is not None:
        cal = int(calories * percent)
        print(f"You ate {cal} calories!")
        add_food_diary_entry(food_name, cal)
    else:
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
