from flask_restful import Resource
from flask import request
from main.repositories.message_repository import MessageRepository
from main.maps.message_schema import MessageSchema
from .. import db


message_repository = MessageRepository()
message_schema = MessageSchema()


class MessagesResource(Resource):
    def get(self):
        messages = message_repository.get_all()
        return message_schema.dump(messages, many = True)

    def post(self):
        session = db.session.session_factory()
        message = message_schema.load(request.get_json(), session=session)
        message_repository.create(message)
        return message_schema.dump(message), "Mensaje Creado"




class MessageResource(Resource):
    def get(self,id):
       message = message_repository.get_by_id(id)
       return message_schema.dump(message)



    def put(self, id):
        message = message_repository.update(id, request.get_json().items())
        return message_schema.dump(message)


    def delete(self, id):
        message_repository.delete(id)
        return 'Mensaje Eliminado'
