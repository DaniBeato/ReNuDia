from flask_restful import Resource
from flask import request
from main.repositories.nutritionist_diabetic_repository import NutritionistDiabeticRepository
from main.maps.nutritionist_diabetic_schema import NutritionistDiabeticSchema
from .. import db
from main.auth.decoradores import login_required, nutritionist_required


nutritionist_diabetic_repository = NutritionistDiabeticRepository()
nutritionist_diabetic_schema = NutritionistDiabeticSchema()



class NutritionistDiabeticsResource(Resource):

    @login_required
    def get(self):
        filters = request.data
        if filters:
            for key, value in request.get_json().items():
                if key == 'nutritionist_id':
                    nutritionist_diabetics = nutritionist_diabetic_repository.get_by_nutritionist_id(value)
        else:
            nutritionist_diabetics = nutritionist_diabetic_repository.get_all()
        return nutritionist_diabetic_schema.dump(nutritionist_diabetics, many = True)

    @nutritionist_required
    def post(self):
        session = db.session.session_factory()
        nutritionist_diabetic = nutritionist_diabetic_schema.load(request.get_json(), session=session)
        if not nutritionist_diabetic_repository.get_by_nutritionist_and_diabetic_id(
            nutritionist_diabetic.nutritionist_id, nutritionist_diabetic.diabetic_id):
            nutritionist_diabetic_repository.create(nutritionist_diabetic)
        else:
            return 'El paciente diabético ya está asignado al nutricionista', 400
        return nutritionist_diabetic_schema.dump(nutritionist_diabetic), 200




class NutritionistDiabeticResource(Resource):

    @login_required
    def get(self,id):
       nutritionist_diabetic = nutritionist_diabetic_repository.get_by_id(id)
       return nutritionist_diabetic_schema.dump(nutritionist_diabetic)


    @nutritionist_required
    def put(self, id):
        nutritionist_diabetic = nutritionist_diabetic_repository.update(id, request.get_json().items())
        return nutritionist_diabetic_schema.dump(nutritionist_diabetic)


    @nutritionist_required
    def delete(self, id):
        nutritionist_diabetic_repository.delete(id)
        return 'Se ha eliminado al paciente diabético del nutricionista'
