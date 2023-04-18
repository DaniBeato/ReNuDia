from flask_restful import Resource
from flask import request
from main.repositories.food_repository import FoodRepository
from main.maps.food_schema import FoodSchema
from .. import db


food_repository = FoodRepository()
food_schema = FoodSchema()

class FoodsResource(Resource):
    def get(self):
        foods = food_repository.get_all()
        return food_schema.dump(foods, many = True)

    def post(self):
        session = db.session.session_factory()
        food = food_schema.load(request.get_json(), session=session)
        food_repository.create(food)
        return food_schema.dump(food), "Comida Creada"


class FoodResource(Resource):
    def get(self,id):
       food = food_repository.get_by_id(id)
       return food_schema.dump(food)


    def put(self, id):
        food = food_repository.update(id, request.get_json().items())
        return food_schema.dump(food)


    def delete(self, id):
        food_repository.delete(id)
        return 'Comida Eliminada'
