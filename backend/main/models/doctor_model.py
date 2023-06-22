from .. import db


class DoctorModel(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    medical_speciality = db.Column(db.String(64), nullable=True)
    doctor_license = db.Column(db.String(64), nullable=True)
    id_card = db.Column(db.String(64), nullable=True)




    def __repr__(self):
        return "<Id: %r, Name: %r, Surname: %r, Medical Speciallity: %r, Doctor License: %r, Id Card: %r>" %(self.id,
                                                                       self.name, self.surname, self.medical_speciality,
                                                                       self.doctor_license,self.id_card)



