from .. import db

class FoodModel(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    amount_sugar = db.Column(db.Integer, nullable=False)
    nutritional_records = db.relationship("NutritionalRecordModel",
                                         primaryjoin="NutritionalRecordModel.food_id==FoodModel.id",
                                         back_populates="food", cascade="all, delete-orphan")



    def __repr__(self):
        return "<Id: %r, Name: %r, Amount of Sugar: %r>" %(self.id, self.name, self.amount_sugar)