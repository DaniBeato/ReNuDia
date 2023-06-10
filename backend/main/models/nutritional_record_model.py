from .. import db

class NutritionalRecordModel(db.Model):
    __tablename__ = 'nutritional records'
    id = db.Column(db.Integer, primary_key=True)
    diabetic_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    amount_food = db.Column(db.String(64), nullable=True)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=True)
    glucose_value = db.Column(db.Integer, nullable=False)
    user = db.relationship("UserModel", back_populates="nutritional_records", uselist=False, single_parent=True)
    food = db.relationship("FoodModel", back_populates="nutritional_records", uselist=False, single_parent=True)


    def __repr__(self):
        return "<Id: %r, User Id: %r, Date: %r, Food Id: %r, Glucose Value: %r>" %(self.id, self.diabetic_id, self.date,\
                                                                                   self.food_id, self.glucose_value)