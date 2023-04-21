from .. import db
from .. models.message_model import MessageModel


class MessageRepository:
    def __init__(self):
        self.messages = MessageModel

    def get_all(self):
        return self.messages.query.all()

    def get_by_id(self, id):
        return self.messages.query.get(id)


    def create(self, message):
        db.session.add(message)
        db.session.commit()
        return message

    def update(self, id, data):
        message = self.messages.query.get(id)
        for key, value in data:
            setattr(message, key, value)
        db.session.add(message)
        db.session.commit()
        return message

    def delete(self, id):
        message = self.messages.query.get(id)
        db.session.delete(message)
        db.session.commit()
        return message