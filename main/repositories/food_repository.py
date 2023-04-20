from .. import db
from .. models.food_model import FoodModel


class FoodRepository:
    def __init__(self):
        self.foods = FoodModel

    def get_all(self):
        return self.foods.query.all()

    def get_by_id(self, id):
        return self.foods.query.get(id)

    def get_by_foodname(self, foodname):
        return self.foods.query.filter_by(name=foodname).all()


    def create(self, food):
        db.session.add(food)
        db.session.commit()
        return food

    def update(self, id, data):
        food = self.foods.query.get(id)
        for key, value in data:
            setattr(food, key, value)
        db.session.add(food)
        db.session.commit()
        return food

    def delete(self, id):
        food = self.foods.query.get(id)
        db.session.delete(food)
        db.session.commit()
        return food
