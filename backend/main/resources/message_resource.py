from flask_restful import Resource
from flask import request
from main.repositories.message_repository import MessageRepository
from main.maps.message_schema import MessageSchema
from .. import db


message_repository = MessageRepository()
message_schema = MessageSchema()
from main.auth.decoradores import login_required


class MessagesResource(Resource):

    @login_required
    def get(self):
        filters = request.data
        if filters:
            for key, value in request.get_json().items():
                if key == 'sender_id':
                    messages_sent = message_repository.get_by_sender_id(int(value))
                if key == 'receptor_id':
                    messages_recept = message_repository.get_by_receptor_id(int(value))
            messages = messages_sent + messages_recept
            messages = message_repository.sort_by_id(messages)
            print(messages)
        else:
            messages = message_repository.get_all()
        return message_schema.dump(messages, many = True)

    @login_required
    def post(self):
        session = db.session.session_factory()
        message = message_schema.load(request.get_json(), session=session)
        message_repository.create(message)
        return message_schema.dump(message), "Mensaje Creado"




class MessageResource(Resource):

    @login_required
    def get(self,id):
       message = message_repository.get_by_id(id)
       return message_schema.dump(message)


    @login_required
    def put(self, id):
        message = message_repository.update(id, request.get_json().items())
        return message_schema.dump(message)


    @login_required
    def delete(self, id):
        message_repository.delete(id)
        return 'Mensaje Eliminado'
