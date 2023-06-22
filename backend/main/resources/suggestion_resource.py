from flask_restful import Resource
from flask import request
from main.services.suggestion_service import SuggestionService
from main.auth.decoradores import login_required

suggestion_service = SuggestionService()



class SuggestionResource(Resource):

    @login_required
    def get(self):
        return suggestion_service.get_suggestion(request.get_json().get('diabetic_id'))




