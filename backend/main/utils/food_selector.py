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

    def select_food(self):
        foods = self.food_schema.dump(self.food_repository.get_all(), many=True)
        aleatory_index_to_food_list = random.randint(0, (len(foods)-1))
        aleatory_food = foods[aleatory_index_to_food_list]
        food = (aleatory_food["name"]).lower()
        return 'Como recomendación, le sugerimos comer ' + food + ' si después de 15 minutos de haber ingerido el alimento sólido\
    su glucosa no ha aumentado. '

