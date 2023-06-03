from flask_restful import Resource
from flask import request
from main.repositories.token_disabled_repository import TokenDisabledRepository
from main.maps.token_disabled_schema import TokenDisabledSchema
from .. import db
from main.auth.decoradores import login_required


token_disabled_repository = TokenDisabledRepository()
token_disabled_schema = TokenDisabledSchema()

class TokensDisabledResource(Resource):

    @login_required
    def get(self):
        filters = request.data
        if filters:
            for key, value in request.get_json().items():
                if key == 'jti':
                    tokens_disabled = token_disabled_repository.get_by_jti(value)
        else:
            tokens_disabled = token_disabled_repository.get_all()
        return token_disabled_schema.dump(tokens_disabled, many = True)

    @login_required
    def post(self):
        session = db.session.session_factory()
        token_disabled = token_disabled_schema.load(request.get_json(), session=session)
        token_disabled_repository.create(token_disabled)
        return token_disabled_schema.dump(token_disabled), 200


class TokenDisabledResource(Resource):

    @login_required
    def get(self,id):
       token_disabled = token_disabled_repository.get_by_id(id)
       return token_disabled_schema.dump(token_disabled)


    @login_required
    def put(self, id):
        token_disabled = token_disabled_repository.update(id, request.get_json().items())
        return token_disabled_schema.dump(token_disabled)

    @login_required
    def delete(self, id):
        token_disabled_repository.delete(id)
        return 'Token Eliminado'
