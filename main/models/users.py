from .. import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128))
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Boolean, nullable=False)
    rol = db.Column(db.Boolean, nullable=False)
    diabetes_type = db.Column(db.String(64), nullable=False)
    doctor_license = db.Column(db.String(64), nullable=False)
    message = db.relationship("messages", back_populates="users", cascade="all, delete-orphan")
    nutritional_record = db.relationship("nutritional records", back_populates="users", cascade="all, delete-orphan")

    def __repr__(self):
        return "<Id: %r, Email: %r, Password: %r, Name: %r, Surname: %r, Age: %r, Weight: %r, Height: %r, Gender: %r, "\
               "Rol: %r, Diabetes' Type: %r, Doctor's  Licence: %r>" %(self.id, self.email, self.password, self.name,
                                                                       self.surname,self.age, self.weight, self.height,
                                                                       self.gender, self.rol, self.diabetes_type,
                                                                       self.doctor_license)