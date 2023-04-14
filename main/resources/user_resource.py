from flask_restful import Resource
from flask import request
from main.repositories.user_repository import UserRepository
from main.maps.user_schema import UserSchema


user_repository = UserRepository()
user_schema = UserSchema()



class UsersResource(Resource):
    def get(self):
        users = user_repository.get_all()
        return user_schema.dump(users.all(), many = True)

    def post(self):
        user = user_schema.load(request.get_json())
        user_repository.create(user)
        return user_schema.dump(user), "Usuario Creado"




class UserResource(Resource):
    def get(self,id):
       user = user_repository.get_by_id(id)
       return user_schema.dump(user)



    def put(self, id):
        user = user_repository.update(id, request.get_json().items())
        return user_schema.dump(user)


    def delete(self, id):
        user_repository.delete(id)
        return 'Usuario Eliminado'
