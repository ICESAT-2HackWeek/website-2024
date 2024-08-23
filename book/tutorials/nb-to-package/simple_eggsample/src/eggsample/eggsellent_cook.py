import random

condiments_tray = ["pickled walnuts", "steak sauce", "mushy peas"]

class EggsellentCook:
    FAVORITE_INGREDIENTS = ("egg", "egg", "egg")

    def __init__(self):
        self.ingredients = None
        
    def _add_ingredients(self, ingredients):
        spices = ["salt", "pepper"]
        you_can_never_have_enough_eggs = ["egg", "egg"]
        spam = ["lovely spam", "wonderous spam"]
        more_spam = ["splendiferous spam", "magnificent spam"]
        ingredients = spices + you_can_never_have_enough_eggs + spam + more_spam
        return ingredients
    
    def _prep_condiments(self, condiments):
        condiments.append("mint sauce")
        return ("Now this is what I call a condiments tray!",)

    def add_ingredients(self):
        results = self._add_ingredients(
            ingredients=self.FAVORITE_INGREDIENTS
        )
        my_ingredients = list(self.FAVORITE_INGREDIENTS)
        self.ingredients = my_ingredients + results

    def prepare_the_food(self):
        random.shuffle(self.ingredients)

    def serve_the_food(self):
        condiment_comments = self._prep_condiments(
            condiments=condiments_tray
        )
        print(f"Your food. Enjoy some {', '.join(self.ingredients)}")
        print(f"Some condiments? We have {', '.join(condiments_tray)}")
        if any(condiment_comments):
            print("\n".join(condiment_comments))

