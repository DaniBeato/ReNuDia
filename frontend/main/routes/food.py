from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request
import requests, json
from ..forms.food_forms import FoodForm
from .auth import token_vencido, diabetic_required, nutritionist_required


food = Blueprint('food', __name__, url_prefix='/food')




@food.route('/foods', methods=['POST', "GET"])
@token_vencido
def foods():
    form = FoodForm()
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    if form.validate_on_submit():
        data = {}
        # datetime.strptime(bolson_json.get('fecha'), '%Y-%m-%dT%H:%M:%S')
        data["name"] = form.name.data
        data["carbohydrates"] = form.carbohydrates.data
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
    return render_template('/foods.html', foods=foods, form=form)  # ,url=url, ths_list=ths_list, url_actual=url_actual)


@food.route('/update_food/<int:food_id>', methods=['POST', "GET"])
@token_vencido
@nutritionist_required
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
        headers=headers
    )
    foods = json.loads(r.text)
    print(foods)

    if form.validate_on_submit():
        data = {}
        # datetime.strptime(bolson_json.get('fecha'), '%Y-%m-%dT%H:%M:%S')
        data["name"] = form.name.data
        data["carbohydrates"] = form.carbohydrates.data
        print(data)
        r = requests.put(
            current_app.config["API_URL"] + '/foods/{}'.format(food_id),
            headers=headers,
            data=json.dumps(data)
        )

        if r.status_code == 200:
            flash('Se ha modificado el alimento', 'success')
            return redirect(url_for('food.foods'))
        else:
            flash('No se pudo modificar el alimento', 'danger')
            return redirect(url_for('food.foods'))

    return render_template('/update_food.html', actual_food=actual_food, foods=foods, form=form)


@food.route('/delete_food/<int:food_id>', methods=["DELETE", "GET"])
@token_vencido
@nutritionist_required
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
        return redirect(url_for('food.foods'))
    else:
        flash('No se pudo eliminar el alimento', 'danger')
        return redirect(url_for('food.foods'))