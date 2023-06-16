from flask_restful import Resource
from flask import request
from main.repositories.doctor_repository import DoctorRepository
from main.maps.doctor_schema import DoctorSchema
from .. import db



doctor_repository = DoctorRepository()
doctor_schema = DoctorSchema()



class DoctorsResource(Resource):

    def get(self):
        doctors = doctor_repository.get_all()
        return doctor_schema.dump(doctors, many = True)




class DoctorResource(Resource):

    def get(self,name, surname, doctor_license, id_card):
       doctor = doctor_repository.get_doctor(name, surname, doctor_license, id_card)
       return doctor_schema.dump(doctor, many=True), 200


