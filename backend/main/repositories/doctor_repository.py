from .. import db
from .. models.doctor_model import DoctorModel


class DoctorRepository():
    def __init__(self):
        self.doctors = DoctorModel

    def get_all(self):
        return self.doctors.query.all()

    def get_doctor(self, name, surname, doctor_license, id_card):
        return self.doctors.query.filter_by(name=name, surname=surname, doctor_license=doctor_license,
                                            id_card=id_card).all()


    def create(self, user):
        db.session.add(user)
        db.session.commit()
        return

