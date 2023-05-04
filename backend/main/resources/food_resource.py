from flask_restful import Resource
from flask import request
from main.repositories.food_repository import FoodRepository
from main.maps.food_schema import FoodSchema
from .. import db
from main.auth.decoradores import login_required


food_repository = FoodRepository()
food_schema = FoodSchema()

class FoodsResource(Resource):

    @login_required
    def get(self):
        foods = food_repository.get_all()
        return food_schema.dump(foods, many = True)

    @login_required
    def post(self):
        session = db.session.session_factory()
        food = food_schema.load(request.get_json(), session=session)
        food_repository.create(food)
        return food_schema.dump(food), "Comida Creada"


class FoodResource(Resource):

    @login_required
    def get(self,id):
       food = food_repository.get_by_id(id)
       return food_schema.dump(food)


    @login_required
    def put(self, id):
        food = food_repository.update(id, request.get_json().items())
        return food_schema.dump(food)

    @login_required
    def delete(self, id):
        food_repository.delete(id)
        return 'Comida Eliminada'
