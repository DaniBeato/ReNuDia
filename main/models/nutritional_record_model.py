from .. import db

class NutritionalRecordModel(db.Model):
    __tablename__ = 'nutritional records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)
    glucose_value = db.Column(db.Integer, nullable=False)
    user = db.relationship("users", back_populates="nutritional records", uselist=False, single_parent=True)
    food = db.relationship("foods", back_populates="nutritional records", uselist=False, single_parent=True)


    def __repr__(self):
        return "<Id: %r, User Id: %r, Date: %r, Food Id: %r, Glucose Value: %r>" %(self.id, self.user_id, self.date,\
                                                                                   self.food_id, self.glucose_value)