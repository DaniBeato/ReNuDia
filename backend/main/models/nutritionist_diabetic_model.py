from .. import db
from werkzeug.security import generate_password_hash, check_password_hash


class NutritionistDiabeticModel(db.Model):
    __tablename__ = 'nutritionist diabetic'
    id = db.Column(db.Integer, primary_key=True)
    nutritionist_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    diabetic_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user_nutritionist = db.relationship("UserModel", foreign_keys=[nutritionist_id],back_populates="nutritionist", uselist=False,
                                   single_parent=True)
    user_diabetic = db.relationship("UserModel", foreign_keys=[diabetic_id], back_populates="diabetic", uselist=False, single_parent=True)

    def __repr__(self):
        return "<Id: %r, Nutritionist id: %r, Diabetic Id: %r>" %(self.id, self.nutritionist_id, self.diabetic_id)



