from flask import Blueprint, render_template, current_app, redirect, url_for, make_response, flash, request
import requests, json
from ..forms.auth_forms import RegisterForm
from flask_login import login_user
from .auth import User

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
def main_view():
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }

    r = requests.get(
        current_app.config["API_URL"] + '/nutritional_records',
        headers=headers,
        )
    users = json.loads(r.text)
    print(users)
    #header = 'Lista de Bolsones Pendientes'
    url = "main.nutritional_record"
    url_actual = "main.nutritional_record"
    ths_list = ["date", "glucose_value", "foods", "users"]
    return render_template('/index.html', objects=users)#,url=url, ths_list=ths_list, url_actual=url_actual)
    #return redirect(url_for('bolson.bolsones_en_venta'))
    #return render_template('/main/Vista_principal(1).html'


@main.route('/register', methods=['POST', "GET"])
def register():
    form = RegisterForm()  # Instanciar formulario
    #form.rol.choices = ["cliente", "proveedor"]
    if form.validate_on_submit():
        data = {}
        data["name"] = form.name.data
        data["surname"] = form.surname.data
        data["age"] = form.age.data
        data["weight"] = form.weight.data
        data["height"] = form.height.data
        data["gender"] = form.gender.data
        data["diabetes_type"] = form.diabetes_type.data
        data["email"] = form.email.data
        data["password"] = form.password.data
        data["rol"] = "nutricionista"
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer"}
        print(data)
        r = requests.post(
            current_app.config["API_URL"] + '/auth/register',
            headers=headers,
            data=json.dumps(data))
        print('response: ', r.text)
        user_data = json.loads(r.text)
        user = User(id=user_data.get("id"), email=user_data.get("email"), rol=user_data.get("rol"))
        login_user(user)
        req = make_response(redirect(url_for('main.main_view')))
        req.set_cookie('access_token', user_data.get("access_token"), httponly=True)
        flash('Registro e inicio de sesión correctos', 'warning')
        return req
    return render_template('/register.html')



@main.route('/login')
def login():
    return render_template('/login.html')


@main.route('/users/<int:id>')
def user(id):
    headers = {
        'content-type': "application/json",
        # 'authorization': "Bearer {}".format(auth)
    }

    r = requests.get(
        current_app.config["API_URL"] + '/users/{}'.format(id),
        headers=headers,
    )
    user = json.loads(r.text)
    print(user)
    # header = 'Lista de Bolsones Pendientes'
    url = "main.nutritional_record"
    url_actual = "main.nutritional_record"
    ths_list = ["date", "glucose_value", "foods", "users"]
    return render_template('/user.html', user=user)  # ,url=url, ths_list=ths_list, url_actual=url_actual)
    # return redirect(url_for('bolson.bolsones_en_venta'))
    # return render_template('/main/Vista_principal(1).html'



@main.route('/messages/<int:user_id>')
def messages(user_id):
    data = {"sender_id": user_id, "receptor_id": user_id}
    headers = {
        'content-type': "application/json",
        # 'authorization': "Bearer {}".format(auth)
    }

    r = requests.get(
        current_app.config["API_URL"] + '/messages',
        headers=headers,
        data=json.dumps(data)
    )
    messages = json.loads(r.text)
    print(messages)
    # header = 'Lista de Bolsones Pendientes'
    url = "main.nutritional_record"
    url_actual = "main.nutritional_record"
    ths_list = ["date", "glucose_value", "foods", "users"]

    return render_template('/messages.html', messages=messages)  # ,url=url, ths_list=ths_list, url_actual=url_actual)
    # return redirect(url_for('bolson.bolsones_en_venta'))
    # return render_template('/main/Vista_principal(1).html'