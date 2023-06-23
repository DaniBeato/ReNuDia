from flask import Blueprint, render_template, current_app, redirect, url_for, make_response, flash, request
import requests, json
from ..forms.auth_forms import PreRegisterForm, NutritionistRegisterForm, DiabeticRegisterForm, LoginForm
from ..forms.nutritional_record_forms import NutritionalRecordForm
from flask_login import login_user, logout_user
from .auth import User, token_vencido, diabetic_required, nutritionist_required
from datetime import date, time
from flask_login import current_user

main = Blueprint('main', __name__, url_prefix='/')


@main.route('/', methods=['POST', "GET"])
def index():
    return render_template('/index.html')


@main.route('/main_diabetic', methods=['POST', "GET"])
@token_vencido
@diabetic_required
def main_diabetic():
    form = NutritionalRecordForm()
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }

    r = requests.get(
        current_app.config["API_URL"] + '/foods',
        headers=headers)
    print(r.text)
    foods = [(item['id'], (item['name'], item['carbohydrates'])) for item in json.loads(r.text)]
    #foods.insert(0, (0, 'Selecione una opción'))
    form.food.choices = foods

    data = {"diabetic_id": current_user.id}
    r = requests.get(
        current_app.config["API_URL"] + '/nutritional_records',
        headers=headers,
        data=json.dumps(data)
    )
    nutritional_records = json.loads(r.text)
    print(nutritional_records)

    if form.validate_on_submit():
        if form.amount_food.data == "" and form.food.data != None:
            flash('Si selecciona un alimento, debe espedificar su cantidad.', 'danger')
            return render_template('/main_diabetic.html', nutritional_records=nutritional_records,
                                   form=form)
        elif form.amount_food.data != "" and form.food.data == None:
            flash('Si especifica una cantidad, debe seleccionar un alimento.', 'danger')
            return render_template('/main_diabetic.html', nutritional_records=nutritional_records,
                                   form=form)
        data = {}
        # datetime.strptime(bolson_json.get('fecha'), '%Y-%m-%dT%H:%M:%S')
        data["date"] = date.strftime(form.date.data, '%Y-%m-%d')
        data["time"] = time.strftime(form.time.data, '%H:%M:%S')
        data["glucose_value"] = form.glucose_value.data
        data["amount_food"] = form.amount_food.data
        data["food_id"] = form.food.data
        data["diabetic_id"] = current_user.id
        print(data)
        r = requests.post(
            current_app.config["API_URL"] + '/nutritional_records',
            headers=headers,
            data=json.dumps(data)
        )
        if r.status_code == 200:
            flash('Se ha guardado el registro nutricional', 'success')
            data = {"diabetic_id": current_user.id}
            r = requests.get(
                current_app.config["API_URL"] + '/suggestion',
                headers=headers,
                data=json.dumps(data))
            flash(json.loads(r.text), 'warning')
            return redirect(url_for('main.main_diabetic'))
        else:
            flash('No se pudo guardar el registro nutricional', 'danger')
    return render_template('/main_diabetic.html', nutritional_records=nutritional_records,
                           form=form)  # ,url=url, ths_list=ths_list, url_actual=url_actual)




@main.route('/main_nutritionist', methods=['POST', "GET"])
@token_vencido
@nutritionist_required
def main_nutritionist():
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }

    data = {"without_nutritionist": True}
    r = requests.get(
        current_app.config["API_URL"] + '/users',
        headers=headers,
        data=json.dumps(data)
    )
    print(r.text)
    diabetics_without_nutritionists = json.loads(r.text)
    print(diabetics_without_nutritionists)
    return render_template('/main_nutritionist.html', diabetics_without_nutritionists=diabetics_without_nutritionists)


@main.route('/preregister', methods=['POST', "GET"])
def preregister():
    form = PreRegisterForm()
    form.rol.choices = ["diabetico", "nutricionista"]
    if form.validate_on_submit():
        if form.rol.data in form.rol.choices:
            if form.rol.data == "diabetico":
                return redirect(url_for('main.diabetic_register'))
            elif form.rol.data == "nutricionista":
                return redirect(url_for('main.nutritionist_register'))
    return render_template('/preregister.html', form=form)


@main.route('/diabetic-register', methods=['POST', "GET"])
def diabetic_register():
    form = DiabeticRegisterForm()
    form.gender.choices = ["Seleccione una opción", "Masculino", "Femenino"]
    if form.validate_on_submit():
        data = {}
        data["name"] = form.name.data
        data["surname"] = form.surname.data
        data["age"] = form.age.data
        data["weight"] = form.weight.data
        data["height"] = form.height.data
        if form.gender.data == "Masculino":
            data["gender"] = "male"
        else:
            data["gender"] = "female"
        data["diabetes_type"] = form.diabetes_type.data
        data["email"] = form.email.data
        data["password"] = form.password.data
        data["rol"] = "diabetic"
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer"}
        print(data)
        r = requests.post(
            current_app.config["API_URL"] + '/auth/register',
            headers=headers,
            data=json.dumps(data))
        print('response: ', r.text)
        if r.status_code == 200:
            user_data = json.loads(r.text)
            user = User(id=user_data.get("id"), email=user_data.get("email"), rol=user_data.get("rol"))
            login_user(user)
            req = make_response(redirect(url_for('main.main_diabetic')))
            req.set_cookie('access_token', user_data.get("access_token"), httponly=True)
            flash('Registro e inicio de sesión correctos', 'success')
            return req
        elif r.status_code == 409:
            flash('El email ingresado ya existe', 'danger')
            return render_template('/diabetic_register.html', form=form)
    return render_template('/diabetic_register.html', form=form)


@main.route('/nutritionist-register', methods=['POST', "GET"])
def nutritionist_register():
    form = NutritionistRegisterForm()
    form.gender.choices = ["Seleccione una opción", "Masculino", "Femenino"]
    if form.validate_on_submit():
        data = {}
        data["name"] = form.name.data
        data["surname"] = form.surname.data
        data["age"] = form.age.data
        if form.gender.data == "Masculino":
            data["gender"] = "male"
        else:
            data["gender"] = "female"
        data["doctor_license"] = form.doctor_license.data
        data["id_card"] = form.id_card.data
        data["email"] = form.email.data
        data["password"] = form.password.data
        data["rol"] = "nutritionist"
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer"}
        print(data)
        r = requests.get(
            current_app.config["API_URL"] + '/doctors/{}'.format(data['name']) + '/{}'.format(data['surname'])
            + '/{}'.format(data['doctor_license']) + '/{}'.format(data['id_card']),
            headers=headers)
        if len(json.loads(r.text)) == 0:
            flash('Usted no es nutricionista, o no se encuentra en el Registro de Profesionales Inscriptos, '
                  'o ha ingresado incorrectamente sus datos.', 'danger')
            return render_template('/nutritionist_register.html', form=form)
        r = requests.post(
            current_app.config["API_URL"] + '/auth/register',
            headers=headers,
            data=json.dumps(data))
        print('response: ', r.text)
        if r.status_code == 200:
            user_data = json.loads(r.text)
            user = User(id=user_data.get("id"), email=user_data.get("email"), rol=user_data.get("rol"))
            login_user(user)
            req = make_response(redirect(url_for('main.main_nutritionist')))
            req.set_cookie('access_token', user_data.get("access_token"), httponly=True)
            flash('Registro e inicio de sesión correctos', 'success')
            return req
        elif r.status_code == 409:
            flash('El email ingresado ya existe', 'danger')
            return render_template('/nutritionist_register.html', form=form)
    return render_template('/nutritionist_register.html', form=form)


@main.route('/login', methods=['POST', "GET"])
def login():
    form = LoginForm()  # Instanciar formulario
    # form.rol.choices = ["cliente", "proveedor"]
    if form.validate_on_submit():
        data = {}
        data["email"] = form.email.data
        data["password"] = form.password.data
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer"}
        print(data)
        r = requests.post(
            current_app.config["API_URL"] + '/auth/login',
            headers=headers,
            data=json.dumps(data))
        print('response: ', r.text)
        if r.status_code == 200:
            user_data = json.loads(r.text)
            user = User(id=user_data.get("id"), email=user_data.get("email"), rol=user_data.get("rol"))
            login_user(user)
            if user_data["rol"] == "diabetic":
                req = make_response(redirect(url_for('main.main_diabetic')))
            elif user_data["rol"] == "nutritionist":
                req = make_response(redirect(url_for('main.main_nutritionist')))
            req.set_cookie('access_token', user_data.get("access_token"), httponly=True)
            flash('Inicio de sesión correcto', 'success')
            return req
        else:
            flash('Email o contraseña incorrectos', 'danger')
            return render_template('/login.html', form=form)
    return render_template('/login.html', form=form)


@main.route('/logout')
@token_vencido
def logout():
    # Crear una request de redirección
    req = make_response(redirect(url_for('main.index')))
    # Vaciar cookie
    req.set_cookie('access_token', '', httponly=True)
    # Deloguear usuario
    logout_user()
    flash('Sesión cerrada con éxito', 'success')
    # Realizar request
    return req


@main.route('/users/<int:id>')
@token_vencido
def user(id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }

    r = requests.get(
        current_app.config["API_URL"] + '/users/{}'.format(id),
        headers=headers,
    )
    user = json.loads(r.text)
    print(user)
    return render_template('/user.html', user=user)




@main.route('/diabetic_info/<int:diabetic_id>')
@token_vencido
@nutritionist_required
def diabetic_info(diabetic_id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }

    r = requests.get(
        current_app.config["API_URL"] + '/users/{}'.format(diabetic_id),
        headers=headers,
    )
    diabetic = json.loads(r.text)
    print(user)
    data = {"diabetic_id": diabetic_id}
    r = requests.get(
        current_app.config["API_URL"] + '/nutritional_records',
        headers=headers,
        data=json.dumps(data)
    )
    nutritional_records = json.loads(r.text)
    return render_template('/diabetic_info.html', nutritional_records=nutritional_records, diabetic=diabetic)




@main.route('/delete_user/<int:id>', methods=["DELETE", "GET"])
@token_vencido
def delete_user(id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }

    r = requests.delete(
        current_app.config["API_URL"] + '/users/{}'.format(id),
        headers=headers,
    )
    if r.status_code == 200:
        flash('Se ha eliminado el usuario', 'success')
        return redirect(url_for('main.logout'))
    else:
        flash('No se pudo eliminar el usuario', 'danger')
        return redirect(url_for('main.user', id=id))


@main.route('/update_diabetic/<int:id>', methods=["POST", "GET"])
@token_vencido
@diabetic_required
def update_diabetic(id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }

    r = requests.get(
        current_app.config["API_URL"] + '/users/{}'.format(id),
        headers=headers,
    )
    user = json.loads(r.text)
    print(user)

    form = DiabeticRegisterForm()
    if user["gender"] == "male":
        form.gender.choices = ["Masculino", "Femenino"]
    else:
        form.gender.choices = ["Femenino", "Masculino"]

    if form.validate_on_submit():
        data = {}
        data["name"] = form.name.data
        data["surname"] = form.surname.data
        data["age"] = form.age.data
        data["weight"] = form.weight.data
        data["height"] = form.height.data
        if form.gender.data == "Masculino":
            data["gender"] = "male"
        else:
            data["gender"] = "female"
        data["diabetes_type"] = form.diabetes_type.data
        data["email"] = form.email.data
        data["password"] = form.password.data
        data["rol"] = "diabetic"
        print(data)
        r = requests.put(
            current_app.config["API_URL"] + '/users/{}'.format(id),
            headers=headers,
            data=json.dumps(data))
        print('response: ', r.status_code)
        if r.status_code == 200:
            flash('Se ha modificado su información', 'success')
            return redirect(url_for('main.user', id=id))
        else:
            flash('Error, ese email ya existe', 'danger')
    return render_template('/update_diabetic.html', form=form, user=user)



@main.route('/update_nutritionist/<int:id>', methods=["POST", "GET"])
@token_vencido
@nutritionist_required
def update_nutritionist(id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }

    r = requests.get(
        current_app.config["API_URL"] + '/users/{}'.format(id),
        headers=headers,
    )
    user = json.loads(r.text)
    print(user)

    form = NutritionistRegisterForm()
    if user["gender"] == "male":
        form.gender.choices = ["Masculino", "Femenino"]
    else:
        form.gender.choices = ["Femenino", "Masculino"]

    if form.validate_on_submit():
        data = {}
        data["name"] = form.name.data
        data["surname"] = form.surname.data
        if form.gender.data == "Masculino":
            data["gender"] = "male"
        else:
            data["gender"] = "female"
        data["doctor_license"] = form.doctor_license.data
        data["id_card"] = form.id_card.data
        data["email"] = form.email.data
        data["password"] = form.password.data
        data["rol"] = "nutritionist"
        print(data)
        r = requests.put(
            current_app.config["API_URL"] + '/users/{}'.format(id),
            headers=headers,
            data=json.dumps(data))
        print('response: ', r.text)
        if r.status_code == 200:
            flash('Se ha modificado su información', 'success')
            return redirect(url_for('main.user', id=id))
        else:
            flash('Error, ese email ya existe', 'success')
    return render_template('/update_nutritionist.html',  user=user, form=form)
