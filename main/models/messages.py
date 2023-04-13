from .. import db

class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(1000), nullable=False)
    user = db.relationship("users", back_populates="messages", uselist=False, single_parent=True)


    def __repr__(self):
        return "<Id: %r, Sender Id: %r, Receptor Id: %r, Message: %r>" %(self.id, self.sender_id, self.receptor_id,\
                                                                         self.message)
