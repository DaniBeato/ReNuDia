from .. import db

class Foods(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    amount_sugar = db.Column(db.Integer, nullable=False)
    nutritional_record = db.relationship("nutritional records", back_populates="foods", cascade="all, delete-orphan")



    def __repr__(self):
        return "<Id: %r, Name: %r, Amount of Sugar: %r>" %(self.id, self.name, self.amount_sugar)