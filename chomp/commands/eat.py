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
        add_food_diary_entry(food_name, dict(calories=cal))
    else:
        try:
            food_details = get_food(food_name)
            if "nutritional_facts" not in food_details or \
               "calories" not in food_details['nutritional_facts']:
                print(f"Can't find calorie information for {food_name}")
                return

            if weight:
                food_weight = food_details["weight"]
                percent = weight / food_weight

            nutritional_facts = food_details['nutritional_facts']
            scaled_facts = _scale_nutritional_facts(nutritional_facts, percent)
            cal = int(nutritional_facts["calories"])
            print(f"You ate {cal} calories!!")
            add_food_diary_entry(food_name, scaled_facts)
        except FoodNotFoundException:
            print(f"Cannot find {food_name}!")

def _scale_nutritional_facts(nutritional_facts, scale):
    scaled_facts = dict()

    for key, value in nutritional_facts.items():
        if type(value) is dict:
            scaled_facts[key] = _scale_nutritional_facts(value, scale)
        else:
            scaled_facts[key] = value * scale
    return scaled_facts
