from .. import db
from .. models.message_model import MessageModel


class MessageRepository:
    def __init__(self):
        self.messages = MessageModel


    def get_all(self):
        return self.messages.query.all()

    def get_by_id(self, id):
        return self.messages.query.get(id)


    def get_by_sender_id(self, sender_id):
        return self.messages.query.filter_by(sender_id=sender_id).order_by(self.messages.id).all()

    def get_by_receptor_id(self, receptor_id):
        return self.messages.query.filter_by(receptor_id=receptor_id).order_by(self.messages.id).all()


    def get_by_sender_id_and_receptor_id(self, sender_id, receptor_id):
        return self.messages.query.filter_by(sender_id=sender_id, receptor_id=receptor_id).order_by(self.messages.id).all()

    def get_all_chat(self, sender_id, receptor_id):
        messages_sent = db.session.query(self.messages).filter_by(sender_id=sender_id, receptor_id=receptor_id)
        messages_recept = db.session.query(self.messages).filter_by(sender_id=receptor_id, receptor_id=sender_id)
        messages = messages_sent.union(messages_recept).order_by(self.messages.id).all()
        return messages


    def sort_by_id(self, messages):
        return sorted(messages, key=lambda x: x.id)

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

    def create_session(self):
        return db.session.query(self.messages)