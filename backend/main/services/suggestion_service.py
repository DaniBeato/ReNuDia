from ..repositories.food_repository import FoodRepository
from ..repositories.nutritional_record_repository import NutritionalRecordRepository
from ..utils.food_selector import FoodSelector
from ..utils.glycemic_status_calculator import GlycemicStatusCalculator


class SuggestionService():
    def __init__(self):
        self.food_repository = FoodRepository()
        self.nutritional_record_repository = NutritionalRecordRepository()
        self.food_selector = FoodSelector()
        self.glycemic_status_calculator = GlycemicStatusCalculator()


    def get_suggestion(self, user_id):
        last_nutritional_record = self.nutritional_record_repository.get_last_nutritional_record(user_id)
        if last_nutritional_record is None:
            return ""
        glycemic_status = self.glycemic_status_calculator.calculate_glycemic_status(last_nutritional_record)
        if glycemic_status == "hypoglycemia":
            food = self.food_selector.select_food(last_nutritional_record)
            return "Tiene muy poca azúcar en sangre, se le recomienda comer " + food['food'] + " en una cantidad de " + \
                str(food['amount']) + " gramos y consultar urgente a su médico nutricionista."
        elif glycemic_status == "hyperglycemia":
            return "Tiene exceso de azúcar en sangre, se le recomienda hacer ejercicio, tomar agua y " \
                   "consultar a su médico nutricionista."
        else:
            return "Su nivel de azúcar en sangre es normal, se le recomienda mantener una dieta balanceada " \
                   "y hacer ejercicio."

