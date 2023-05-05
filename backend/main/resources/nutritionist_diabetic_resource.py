from flask_restful import Resource
from flask import request
from main.repositories.nutritionist_diabetic_repository import NutritionistDiabeticRepository
from main.maps.nutritionist_diabetic_schema import NutritionistDiabeticSchema
from .. import db
from main.auth.decoradores import login_required


nutritionist_diabetic_repository = NutritionistDiabeticRepository()
nutritionist_diabetic_schema = NutritionistDiabeticSchema()



class NutritionistDiabeticsResource(Resource):

    #@login_required
    def get(self):
        nutritionist_diabetics = nutritionist_diabetic_repository.get_all()
        return nutritionist_diabetic_schema.dump(nutritionist_diabetics, many = True)

    #@login_required
    def post(self):
        session = db.session.session_factory()
        nutritionist_diabetic = nutritionist_diabetic_schema.load(request.get_json(), session=session)
        nutritionist_diabetic_repository.create(nutritionist_diabetic)
        return nutritionist_diabetic_schema.dump(nutritionist_diabetic), "Se ha anexado el paciente diabético" \
                                                                         " al nutricionista"




class NutritionistDiabeticResource(Resource):

    @login_required
    def get(self,id):
       nutritionist_diabetic = nutritionist_diabetic_repository.get_by_id(id)
       return nutritionist_diabetic_schema.dump(nutritionist_diabetic)


    @login_required
    def put(self, id):
        nutritionist_diabetic = nutritionist_diabetic_repository.update(id, request.get_json().items())
        return nutritionist_diabetic_schema.dump(nutritionist_diabetic)


    @login_required
    def delete(self, id):
        nutritionist_diabetic_repository.delete(id)
        return 'Se ha eliminado al paciente diabético del nutricionista'
