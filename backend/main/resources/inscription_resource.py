from flask_restful import Resource
from flask import request
from main.repositories.inscription_repository import InscriptionRepository
from main.maps.inscription_schema import InscriptionSchema
from .. import db
from main.auth.decoradores import login_required, nutritionist_required


inscription_repository = InscriptionRepository()
inscription_schema = InscriptionSchema()



class InscriptionsResource(Resource):

    @login_required
    def get(self):
        filters = request.data
        if filters:
            for key, value in request.get_json().items():
                if key == 'nutritionist_id':
                    inscriptions = inscription_repository.get_by_nutritionist_id(value)
                if key == 'diabetic_id':
                    inscriptions = inscription_repository.get_by_diabetic_id(value)
        else:
            inscriptions = inscription_repository.get_all()
        return inscription_schema.dump(inscriptions, many = True)

    @nutritionist_required
    def post(self):
        session = db.session.session_factory()
        inscription = inscription_schema.load(request.get_json(), session=session)
        if not inscription_repository.get_by_nutritionist_and_diabetic_id(
            inscription.nutritionist_id, inscription.diabetic_id):
            inscription_repository.create(inscription)
        else:
            return 'El paciente diabético ya está asignado al nutricionista', 400
        return inscription_schema.dump(inscription), 200




class InscriptionResource(Resource):

    @login_required
    def get(self,id):
       inscription = inscription_repository.get_by_id(id)
       return inscription_schema.dump(inscription)


    @nutritionist_required
    def put(self, id):
        inscription = inscription_repository.update(id, request.get_json().items())
        return inscription_schema.dump(inscription)


    @nutritionist_required
    def delete(self, id):
        inscription_repository.delete(id)
        return 'Se ha eliminado al paciente diabético del nutricionista'
