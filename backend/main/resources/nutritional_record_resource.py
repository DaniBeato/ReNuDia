from flask_restful import Resource
from flask import request
from main.repositories.nutritional_record_repository import NutritionalRecordRepository
from main.maps.nutritional_record_schema import NutritionalRecordSchema
from .. import db
from main.auth.decoradores import login_required


nutritional_record_repository = NutritionalRecordRepository()
nutritional_record_schema = NutritionalRecordSchema()



class NutritionalRecordsResource(Resource):

    @login_required
    def get(self):
        filters = request.data
        if filters:
            for key, value in request.get_json().items():
                if key == 'diabetic_id':
                    nutritional_records = nutritional_record_repository.get_by_diabetic_id(int(value))
        else:
            nutritional_records = nutritional_record_repository.get_all()
        return nutritional_record_schema.dump(nutritional_records, many = True), 200

    @login_required
    def post(self):
        session = db.session.session_factory()
        nutritional_record = nutritional_record_schema.load(request.get_json(), session=session)
        nutritional_record_repository.create(nutritional_record)
        return nutritional_record_schema.dump(nutritional_record), 200




class NutritionalRecordResource(Resource):

    @login_required
    def get(self,id):
       nutritional_record = nutritional_record_repository.get_by_id(id)
       return nutritional_record_schema.dump(nutritional_record)


    @login_required
    def put(self, id):
        nutritional_record = nutritional_record_repository.update(id, request.get_json().items())
        return nutritional_record_schema.dump(nutritional_record)


    @login_required
    def delete(self, id):
        nutritional_record_repository.delete(id)
        return 'Ficha Nutricional Eliminada'
