
from flask import request, jsonify, Blueprint
from .. import db
from main.models import UserModel
from main.maps import UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt
from datetime import datetime
import os

user_schema = UserSchema()
user_model = UserModel()



auth = Blueprint('auth', __name__, url_prefix = '/auth')


@auth.route('/login', methods = ['POST'])
def login():
    user = db.session.query(user_model).filter(user_model.mail == request.get_json().get("email")).first_or_404()
    if user.validation_password(request.get_json().get("password")):
        access_token = create_access_token(identity = user)
        data = {
            str('id'): user.id,
            'email': user.mail,
            'access_token': access_token,
            'rol': user.rol
        }
        return data, 200
    else:
        return 'Contraseña incorrecta', 401

@auth.route('/register', methods = ['POST'])
def register():
    user = user_schema.load(request.get_json())
    exist = db.session.query(user_model).filter(user_model.mail == user.email).scalar() is not None
    if exist:
        return 'Email duplicado', 409
    else:
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()
            return str(error), 409
        return user_schema.dump(user), 201









