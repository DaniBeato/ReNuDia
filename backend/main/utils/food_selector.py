from ..repositories.food_repository import FoodRepository
from ..repositories.nutritional_record_repository import NutritionalRecordRepository
from ..utils.glycemic_status_calculator import GlycemicStatusCalculator
import random
from .. maps.food_schema import FoodSchema
from ..repositories.food_repository import FoodRepository




class FoodSelector():

    def __init__(self):
        self.food_schema = FoodSchema()
        self.food_repository = FoodRepository()

    def select_food(self, last_nutritional_record):
        foods = self.food_schema.dump(self.food_repository.get_all(), many=True)
        actual_glucose_value = last_nutritional_record['glucose_value']
        print(actual_glucose_value)
        missing_glucose_value = 150 - actual_glucose_value
        aleatory_index_to_food_list = random.randint(0, (len(foods)-1))
        aleatory_food = foods[aleatory_index_to_food_list]
        aleatory_food_amount = (missing_glucose_value / aleatory_food['carbohydrates']) * 100
        food = {"food": aleatory_food["name"], "amount": int(aleatory_food_amount)}
        print(food)
        return food

