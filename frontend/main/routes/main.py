from flask import Blueprint, render_template, current_app, redirect, url_for, make_response, flash, request
import requests, json
from ..forms.auth_forms import PreRegisterForm, NutritionistRegisterForm, DiabeticRegisterForm, LoginForm
from ..forms.nutritional_record_forms import NutritionalRecordForm
from ..forms.food_forms import FoodForm
from flask_login import login_user
from .auth import User
from datetime import datetime, date, time
from flask_login import current_user

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/' , methods=['POST', "GET"])
def main_view():
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
    foods = [(item['id'], (item['name'], item['amount_sugar'])) for item in json.loads(r.text)]
    foods.insert(0, (0, ''))
    form.food.choices = foods

    if form.validate_on_submit():
        data = {}
        #datetime.strptime(bolson_json.get('fecha'), '%Y-%m-%dT%H:%M:%S')
        data["date"] = date.strftime(form.date.data, '%Y-%m-%d') + "T" + time.strftime(form.time.data, '%H:%M:%S')
        data["glucose_value"] = form.glucose_value.data
        data["food_id"] = form.food.data
        data["user_id"] = current_user.id
        print(data)
        r = requests.post(
            current_app.config["API_URL"] + '/nutritional_records',
            headers=headers,
            data=json.dumps(data)
        )
    data = {"user_id": current_user.id}
    r = requests.get(
        current_app.config["API_URL"] + '/nutritional_records',
        headers=headers,
        data=json.dumps(data)
    )
    users = json.loads(r.text)
    print(users)
    return render_template('/index.html', objects=users, form=form)#,url=url, ths_list=ths_list, url_actual=url_actual)



@main.route('/main_diabetic' , methods=['POST', "GET"])
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
    foods = [(item['id'], (item['name'], item['amount_sugar'])) for item in json.loads(r.text)]
    foods.insert(0, (0, ''))
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
        data = {}
        #datetime.strptime(bolson_json.get('fecha'), '%Y-%m-%dT%H:%M:%S')
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
        else:
            flash('No se pudo guardar el registro nutricional', 'danger')
    return render_template('/main_diabetic.html', nutritional_records=nutritional_records, form=form)#,url=url, ths_list=ths_list, url_actual=url_actual)



@main.route('/update_nutritional_record/<int:nutritional_record_id>' , methods=['POST', "GET"])
def update_nutritional_record(nutritional_record_id):
    form = NutritionalRecordForm()
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }

    r = requests.get(
        current_app.config["API_URL"] + '/nutritional_records/{}'.format(nutritional_record_id),
        headers=headers,
    )
    actual_nutritional_record = json.loads(r.text)
    print(r.text)

    data = {"diabetic_id": current_user.id}
    r = requests.get(
        current_app.config["API_URL"] + '/nutritional_records',
        headers=headers,
        data=json.dumps(data)
    )
    nutritional_records = json.loads(r.text)

    r = requests.get(
        current_app.config["API_URL"] + '/foods',
        headers=headers)
    print(r.text)
    foods = [(item['id'], (item['name'], item['amount_sugar'])) for item in json.loads(r.text)]
    foods.insert(0, (0, ''))
    form.food.choices = foods

    if form.validate_on_submit():
        data = {}
        data["date"] = date.strftime(form.date.data, '%Y-%m-%d')
        data["time"] = time.strftime(form.time.data, '%H:%M:%S')
        data["glucose_value"] = form.glucose_value.data
        data["amount_food"] = form.amount_food.data
        data["food_id"] = form.food.data
        data["diabetic_id"] = current_user.id
        print(data)
        r = requests.put(
            current_app.config["API_URL"] + '/nutritional_records/{}'.format(nutritional_record_id),
            headers=headers,
            data=json.dumps(data)
        )
        if r.status_code == 200:
            flash('Se ha modificado el registro nutricional', 'success')
            return redirect(url_for('main.main_diabetic'))
        else:
            flash('No se pudo modificar el registro nutricional', 'danger')
            return redirect(url_for('main.main_diabetic'))
    return render_template('/update_nutritional_record.html', nutritional_records=nutritional_records , actual_nutritional_record=actual_nutritional_record, form=form)




@main.route('/delete_nutritional_record/<int:nutritional_record_id>' , methods=["DELETE", "GET"])
def delete_nutritional_record(nutritional_record_id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    r = requests.delete(
        current_app.config["API_URL"] + '/nutritional_records/{}'.format(nutritional_record_id),
        headers=headers,
    )
    print(r.text)
    if r.status_code == 200:
        flash('Se ha eliminado el registro nutricional', 'success')
        return redirect(url_for('main.main_diabetic'))
    else:
        flash('No se pudo eliminar el registro nutricional', 'danger')
        return redirect(url_for('main.main_diabetic'))





@main.route('/main_nutritionist' , methods=['POST', "GET"])
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
    form.gender.choices = ["masculino", "femenino"]
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
        else:
            flash('El email ingresado ya existe', 'danger')
            return render_template('/diabetic_register.html', form=form)
    return render_template('/diabetic_register.html', form=form)




@main.route('/nutritionist-register', methods=['POST', "GET"])
def nutritionist_register():
    form = NutritionistRegisterForm()
    form.gender.choices = ["masculino", "femenino"]
    if form.validate_on_submit():
        data = {}
        data["name"] = form.name.data
        data["surname"] = form.surname.data
        data["age"] = form.age.data
        data["gender"] = form.gender.data
        data["doctor_license"] = form.doctor_license.data
        data["email"] = form.email.data
        data["password"] = form.password.data
        data["rol"] = "nutritionist"
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
        else:
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


@main.route('/users/<int:id>')
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


@main.route('/add_diabetic_to_nutritionist/<int:diabetic_id>', methods=['POST', "GET"])
def add_diabetic_to_nutritionist(diabetic_id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    data = {"diabetic_id": diabetic_id, "nutritionist_id": current_user.id}

    r = requests.post(
        current_app.config["API_URL"] + '/inscriptions',
        headers=headers,
        data=json.dumps(data)
    )
    if r.status_code == 200:
        flash('Paciente agregado correctamente', 'success')
        return redirect(url_for('main.main_nutritionist'))
    else:
        flash('No se pudo agregar al paciente', 'danger')
        return redirect(url_for('main.main_nutritionist'))


@main.route('/inscriptions_of_nutritionist_list', methods=['POST', "GET"])
def inscriptions_of_nutritionist_list():
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }

    data = {"nutritionist_id": current_user.id}
    r = requests.get(
        current_app.config["API_URL"] + '/inscriptions',
        headers=headers,
        data=json.dumps(data)
    )
    print(r.text)
    inscriptions_of_nutritionist = json.loads(r.text)
    print(inscriptions_of_nutritionist)
    return render_template('/inscriptions_of_nutritionist_list.html',
                           inscriptions_of_nutritionist=inscriptions_of_nutritionist)  # ,url=url, ths_list=ths_list, url_actual=url_actual)



@main.route('/diabetic_info/<int:diabetic_id>')
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



@main.route('/foods' , methods=['POST', "GET"])
def foods():
    form = FoodForm()
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    if form.validate_on_submit():
        data = {}
        #datetime.strptime(bolson_json.get('fecha'), '%Y-%m-%dT%H:%M:%S')
        data["name"] = form.name.data
        data["amount_sugar"] = form.amount_sugar.data
        print(data)
        r = requests.post(
            current_app.config["API_URL"] + '/foods',
            headers=headers,
            data=json.dumps(data)
        )
        if r.status_code == 200:
            flash('Se ha guardado el alimento', 'success')
        else:
            flash('No se pudo guardar el alimento', 'danger')

    r = requests.get(
        current_app.config["API_URL"] + '/foods',
        headers=headers,
    )
    foods = json.loads(r.text)
    print(foods)
    return render_template('/foods.html', foods=foods, form=form)#,url=url, ths_list=ths_list, url_actual=url_actual)



@main.route('/update_food/<int:food_id>' , methods=['POST', "GET"])
def update_food(food_id):
    form = FoodForm()
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }

    r = requests.get(
        current_app.config["API_URL"] + '/foods/{}'.format(food_id),
        headers=headers,
    )
    actual_food = json.loads(r.text)
    print(r.text)

    r = requests.get(
        current_app.config["API_URL"] + '/foods',
        headers=headers,
    )
    foods = json.loads(r.text)

    if form.validate_on_submit():
        data = {}
        #datetime.strptime(bolson_json.get('fecha'), '%Y-%m-%dT%H:%M:%S')
        data["name"] = form.name.data
        data["amount_sugar"] = form.amount_sugar.data
        print(data)
        r = requests.put(
            current_app.config["API_URL"] + '/foods/{}'.format(food_id),
            headers=headers,
            data=json.dumps(data)
        )
        if r.status_code == 200:
            flash('Se ha modificado el alimento', 'success')
            return redirect(url_for('main.foods'))
        else:
            flash('No se pudo modificar el alimento', 'danger')
            return redirect(url_for('main.foods'))
    return render_template('/update_food.html', actual_food=actual_food, foods=foods, form=form)#,url=url, ths_list=ths_list, url_actual=url_actual)




@main.route('/delete_food/<int:food_id>' , methods=["DELETE", "GET"])
def delete_food(food_id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    r = requests.delete(
        current_app.config["API_URL"] + '/foods/{}'.format(food_id),
        headers=headers,
    )
    print(r.text)
    if r.status_code == 200:
        flash('Se ha eliminado el alimento', 'success')
        return redirect(url_for('main.foods'))
    else:
        flash('No se pudo eliminar el alimento', 'danger')
        return redirect(url_for('main.foods'))

