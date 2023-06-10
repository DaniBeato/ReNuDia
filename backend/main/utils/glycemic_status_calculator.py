class GlycemicStatusCalculator():

    def calculate_glycemic_status(self, last_nutritional_record):
        if last_nutritional_record['amount_food'] is None:
            return self.calculate_without_food(last_nutritional_record['glucose_value'])
        else:
            return self.calculate_with_food(last_nutritional_record['glucose_value'])

    def calculate_with_food(self, glucose_value):
        if glucose_value >= 130:
            return "hyperglycemia"
        elif glucose_value <= 90:
            return "hypoglycemia"
        else:
            return "normal glycemia"

    def calculate_without_food(self, glucose_value):
        if glucose_value >= 180:
            return "hyperglycemia"
        elif glucose_value <= 126:
            return "hypoglycemia"
        else:
            return "normal glycemia"


