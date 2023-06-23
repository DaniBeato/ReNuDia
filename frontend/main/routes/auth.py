from .. import login_manager
from flask import request, flash, redirect, url_for,current_app
from flask_login import UserMixin, LoginManager, current_user
import jwt
from functools import wraps

class User(UserMixin):
    def __init__(self, id, email, rol):
        self.id = id
        self.email = email
        self.rol = rol




@login_manager.request_loader
def load_user(request):
    if 'access_token' in request.cookies:
        try:
            decoded = jwt.decode(request.cookies['access_token'], current_app.config["SECRET_KEY"], algorithms=["HS256"]
                                 , verify=False)
            user = User(decoded["id"], decoded["email"], decoded["rol"])
            return user
        except jwt.exceptions.InvalidTokenError:
            print('Token Inválido')
        except jwt.exceptions.DecodeError:
            print('Error de Decodificación')
    return None


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Debe iniciar sesión para continuar','warning')
    return redirect((url_for('main.login')))



def nutritionist_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.rol == "nutritionist":
            flash('Acceso restringido a médicos nutricionistas.','danger')
            return redirect(url_for('main.main_diabetic'))
        return fn(*args, **kwargs)
    return wrapper


def diabetic_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.rol == "diabetic":
            flash('Acceso restringido a pacientes diabéticos.', 'danger')
            return redirect(url_for('main.main_nutritionist'))
        return fn(*args, **kwargs)
    return wrapper



def token_vencido(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.is_anonymous:
            flash('Debe iniciar sesión para continuar', 'warning')
            return redirect((url_for('main.index')))
        return fn(*args, **kwargs)
    return wrapper

