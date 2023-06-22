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
            return
        glycemic_status = self.glycemic_status_calculator.calculate_glycemic_status(last_nutritional_record)
        if glycemic_status == "hypoglycemia":
            food = self.food_selector.select_food()
            return "Tiene muy poca azúcar en sangre, beba urgentemente un vaso de bebida azucarada, y después coma un " \
                   "alimento sólido. " + food + "Cuando sus niveles de azúcar en sangre se normalicen, se le recomienda " \
                      "consultar a su nutricionista."
        elif glycemic_status == "hyperglycemia":
            return "Tiene exceso de azúcar en sangre, se le recomienda beber agua, tomar su medicación  y " \
                   "consultar a su  nutricionista."
        else:
            return "Su nivel de azúcar en sangre es normal, se le recomienda mantener una dieta equilibrada " \
                   "y hacer ejercicio regularmente. No deje de tomar su medicación y consultar a su médico nutricionista."

