from flask_restful import Resource
from flask import request
from main.repositories.nutritional_record_repository import NutritionalRecordRepository
from main.maps.nutritional_record_schema import NutritionalRecordSchema


nutritional_record_repository = NutritionalRecordRepository()
nutritional_record_schema = NutritionalRecordSchema()



class NutritionalRecordResource(Resource):
    def get(self):
        nutritional_records = nutritional_record_repository.get_all()
        return nutritional_record_schema.dump(nutritional_records.all(), many = True)

    def post(self):
        nutritional_record = request.get_json().items()
        nutritional_record_repository.create(nutritional_record)
        return nutritional_record_schema.dump(nutritional_record), "Registro Nutricional Creado"




class NutritionalRecordsResource(Resource):
    def get(self,id):
       nutritional_record = nutritional_record_repository.get_by_id(id)
       return nutritional_record_schema.dump(nutritional_record)



    def put(self, id):
        nutritional_record = nutritional_record_repository.update(id, request.get_json().items())
        return nutritional_record_schema.dump(nutritional_record)


    def delete(self, id):
        nutritional_record_repository.delete(id)
        return 'Usuario Eliminado'
