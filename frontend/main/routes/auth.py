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
    return redirect((url_for('main.vista_principal')))


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.rol == "admin":
            flash('Acceso restringido a administradores.', 'warning')
            return redirect(url_for('main.vista_principal'))
        return fn(*args, **kwargs)
    return wrapper


def nutritionist_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.rol == "nutricionista":
            flash('Acceso restringido a nutricionistas.','warning')
            return redirect(url_for('main.vista_principal'))
        return fn(*args, **kwargs)
    return wrapper


def diabetic_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.rol == "diabetico":
            flash('Acceso restringido a [acientes diabéticos].', 'warning')
            return redirect(url_for('main.vista_principal'))
        return fn(*args, **kwargs)
    return wrapper


def admin_or_nutritionist(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.rol != "admin" and  current_user.rol != "nutricionista":
            flash('Acceso restringido a administradores o nutricionistas.', 'warning')
            return redirect(url_for('main.vista_principal'))
        return fn(*args, **kwargs)
    return wrapper



def admin_or_diabetic(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.rol != "admin" and current_user.rol != "diabetico":
            flash('Acceso restringido a administradores y pacientes diabéticos.', 'warning')
            return redirect(url_for('main.vista_principal'))
        return fn(*args, **kwargs)
    return wrapper


def token_vencido(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.is_anonymous:
            flash('Debe iniciar sesión para continuar', 'warning')
            return redirect((url_for('main.login')))
        return fn(*args, **kwargs)
    return wrapper

