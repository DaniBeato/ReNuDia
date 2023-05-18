from .message_model import MessageModel
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128))
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(64), nullable=False)
    rol = db.Column(db.String(64), nullable=False)
    diabetes_type = db.Column(db.String(64), nullable=True)
    doctor_license = db.Column(db.String(64), nullable=True)
    messages_sent = db.relationship("MessageModel", back_populates="senders",
                                    primaryjoin="MessageModel.sender_id==UserModel.id", cascade="all, delete-orphan")
    messages_recept = db.relationship("MessageModel", back_populates="receptors",
                                    primaryjoin="MessageModel.receptor_id==UserModel.id", cascade="all, delete-orphan")
    nutritional_records = db.relationship("NutritionalRecordModel",
                                         primaryjoin="NutritionalRecordModel.user_id==UserModel.id",
                                         back_populates="users", cascade="all, delete-orphan")
    nutritionist = db.relationship("NutritionistDiabeticModel", back_populates="user_nutritionist",
                                   primaryjoin="UserModel.id==NutritionistDiabeticModel.nutritionist_id",
                                   cascade="all, delete-orphan")
    diabetic = db.relationship("NutritionistDiabeticModel", back_populates="user_diabetic",
                               primaryjoin="UserModel.id==NutritionistDiabeticModel.diabetic_id",
                               cascade="all, delete-orphan")



    def __repr__(self):
        return "<Id: %r, Email: %r, Password: %r, Name: %r, Surname: %r, Age: %r, Weight: %r, Height: %r, Gender: %r, "\
               "Rol: %r, Diabetes' Type: %r, Doctor's  Licence: %r>" %(self.id, self.email, self.password, self.name,
                                                                       self.surname,self.age, self.weight, self.height,
                                                                       self.gender, self.rol, self.diabetes_type,
                                                                       self.doctor_license)


