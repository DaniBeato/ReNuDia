from .. import db
from .. models.nutritionist_diabetic_model import NutritionistDiabeticModel


class NutritionistDiabeticRepository:
    def __init__(self):
        self.nutritional_diabetics = NutritionistDiabeticModel

    def get_all(self):
        return self.nutritional_diabetics.query.all()

    def get_by_id(self, id):
        return self.nutritional_diabetics.query.get(id)

    def get_by_nutritionist_and_diabetic_id(self, nutritionist_id, diabetic_id):
        return self.nutritional_diabetics.query.filter_by(
            nutritionist_id = nutritionist_id, diabetic_id = diabetic_id).first()

    def get_by_nutritionist_id(self, nutritionist_id):
        return self.nutritional_diabetics.query.filter_by(nutritionist_id = nutritionist_id).all()



    def create(self, nutritional_diabetic):
        db.session.add(nutritional_diabetic)
        db.session.commit()
        return nutritional_diabetic


    def update(self, id, data):
        nutritional_diabetic = self.nutritional_diabetics.query.get(id)
        for key, value in data:
            setattr(nutritional_diabetic, key, value)
        db.session.add(nutritional_diabetic)
        db.session.commit()
        return nutritional_diabetic


    def delete(self, id):
        nutritional_diabetic = self.nutritional_diabetics.query.get(id)
        db.session.delete(nutritional_diabetic)
        db.session.commit()
        return nutritional_diabetic
