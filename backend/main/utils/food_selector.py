from ..repositories.food_repository import FoodRepository
from ..repositories.nutritional_record_repository import NutritionalRecordRepository
from ..utils.glycemic_status_calculator import GlycemicStatusCalculator
import random

class FoodSelector():

    def select_food(self, last_nutritional_record, food_list):
        actual_glucose_value = last_nutritional_record['glucose_value']
        missing_glucose_value = 150 - actual_glucose_value
        aleatory_index_to_food_list = random.randint(0, (len(food_list)-1))
        aleatory_food = food_list[aleatory_index_to_food_list]
        aleatory_food_amount = (aleatory_food['amount_sugar'] / missing_glucose_value) * 100
        food = {"food": aleatory_food["name"], "amount": aleatory_food_amount}
        return food

