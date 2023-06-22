class GlycemicStatusCalculator():

    def calculate_glycemic_status(self, last_nutritional_record):
        if last_nutritional_record["glucose_value"] >= 200:
            return "hyperglycemia"
        elif last_nutritional_record["glucose_value"] <= 70:
            return "hypoglycemia"
        else:
            return "normal glycemia"



