from flask_restful import Resource
from flask import request
from main.repositories.message_repository import MessageRepository
from main.maps.message_schema import MessageSchema
from .. import db
from main.auth.decoradores import login_required

message_repository = MessageRepository()
message_schema = MessageSchema()



class AllChatResource(Resource):

    @login_required
    def get(self):
        if 'sender_id' in request.get_json() and 'receptor_id' in request.get_json():
            for key, value in request.get_json().items():
                if key == 'sender_id':
                    sender_id = int(value)
                if key == 'receptor_id':
                    receptor_id = int(value)
            messages = message_repository.get_all_chat(sender_id, receptor_id)
            return message_schema.dump(messages, many=True)
        return 'Falta especificar sender_id y receptor_id'


class MessagesResource(Resource):

    @login_required
    def get(self):
        messages = message_repository.create_session()
        filters = request.data
        if filters:
            for key, value in request.get_json().items():
                if key == 'sender_id':
                    messages = message_repository.get_by_sender_id(int(value))
                if key == 'receptor_id':
                    messages = message_repository.get_by_receptor_id(int(value))
        else:
            messages = message_repository.get_all()
        return message_schema.dump(messages, many=True)

    @login_required
    def post(self):
        session = db.session.session_factory()
        message = message_schema.load(request.get_json(), session=session)
        message_repository.create(message)
        return message_schema.dump(message), 200


class MessageResource(Resource):

    @login_required
    def get(self, id):
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
