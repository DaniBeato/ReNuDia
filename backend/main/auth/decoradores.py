from .. import jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from .. import db



def nutritionist_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['rol'] == "nutricionista":
            return fn(*args, **kwargs)
        else:
            return 'Solo nutricionistas tienen acceso', 404
    return wrapper



def diabetic_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['rol'] == "diabetico":
            return fn(*args, **kwargs)
        else:
            return 'Solo pacientes diabéticos tienen acceso', 404
    return wrapper




def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['rol'] == "admin":
            return fn(*args, **kwargs)
        else:
            return 'Solo administradores tienen acceso', 404
    return wrapper




def admin_or_diabetic_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['rol'] == "admin":
            return fn(*args, **kwargs)
        else:
            if claims['rol'] == "diabetico":
                return fn(*args, **kwargs)
            else:
                return 'Solo administradores o pacientes diabéticos tienen acceso', 404
    return wrapper



def admin_or_nutricionist_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['rol'] == "admin":
            return fn(*args, **kwargs)
        else:
            if claims['rol'] == "nutricionista":
                return fn(*args, **kwargs)
            else:
                return 'Solo administradores o nutricionistas tienen acceso', 404
    return wrapper




def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['rol'] == "admin":
            return fn(*args, **kwargs)
        else:
            if claims['rol'] == "nutricionista":
                return fn(*args, **kwargs)
            else:
                if claims['rol'] == "nutricionista":
                    return fn(*args, **kwargs)
                return 'Debe iniciar sesión para poder acceder', 404
    return wrapper


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.additional_claims_loader
def add_claims_to_access_token(user):
    claims = {
        'rol': user.rol,
        'id': user.id,
        'email': user.email
    }
    return claims



