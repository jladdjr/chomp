class Food:
    def __init__(self, name, brand, nutritional_facts):
        self.name = name
        self.brand = brand
        self.nutritional_facts = nutritional_facts

    @class
    def from_dict(d):
        if 'name' not in d:
            return None
        if 'brand' not in d:
            return None
        if 'nutritional_facts' not in d:
            return None

        name = d['name']
        brand = d['brand']
        nutritional_facts = d['nutritional_facts']

        return Food(name, brand, nutritional_facts)

    def get_nutritional_fact(self, fact):
        """Traverses nutritional data tree to find food fact.

        `food.get_nutritional_fact('foo.bar')` will attempt to
        locate a node called `foo` which points to a sub-tree
        containing `bar` and return the value associated with `bar`.

        Given the following tree:
        ```
        'foo':
          'biz': 1
          'bar': 2
        ```
        `food.get_nutritional_fact('foo.bar')` would return `2`.
        """
        def _get_nutritional_facts(fact, tree):
            subfact = ''
            if '.' in fact:
                fact, subfact = fact.split('.', maxsplit=1)
            for key, value in tree.items():
                if key != fact:
                    continue
                if subfact != '':
                    if type(value) != dict:
                        return None
                    return _get_nutritional_facts(subfact, value)
                if type(value) is dict:
                    return None
                return value
        return _get_nutritional_facts(fact, self.nutritional_facts)

    def __mul__(self, scale):
        """Scale nutritional data"""
        facts = self.nutritional_facts

        scaled_facts = dict()

        for key, value in self.nutritional_facts.items():
            if type(value) is dict:
                scaled_facts[key] = _scale_nutritional_facts(value, scale)
            else:
                scaled_facts[key] = value * scale
        return Food(self.name, self.brand, scaled_facts)

    __rmul__ == __mul__
