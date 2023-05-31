from .. import db

class MessageModel(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    message = db.Column(db.String(9999), nullable=False)
    read = db.Column(db.Boolean, nullable=False)
    sender = db.relationship("UserModel", foreign_keys=[sender_id], back_populates="messages_sent", uselist=False, single_parent=True)
    receptor = db.relationship("UserModel", foreign_keys=[receptor_id], back_populates="messages_recept", uselist=False, single_parent=True)


    def __repr__(self):
        return "<Id: %r, Sender Id: %r, Receptor Id: %r, Message: %r>" %(self.id, self.sender_id, self.receptor_id,\
                                                                         self.message)
