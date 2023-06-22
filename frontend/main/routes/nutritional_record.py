from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request
import requests, json
from ..forms.nutritional_record_forms import NutritionalRecordForm
from .auth import token_vencido, diabetic_required, nutritionist_required
from datetime import datetime, date, time
from flask_login import current_user

nutritional_record = Blueprint('nutritional_record', __name__, url_prefix='/nutritional_record')



@nutritional_record.route('/update_nutritional_record/<int:nutritional_record_id>', methods=['POST', "GET"])
@token_vencido
@diabetic_required
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

    foods = [(item['id'], (item['name'], item['carbohydrates'])) for item in json.loads(r.text)]
    if (actual_nutritional_record['food']) is not None:
        foods.remove((actual_nutritional_record['food']['id'],
                  (actual_nutritional_record['food']['name'], actual_nutritional_record['food']['carbohydrates'])))
        foods.append(("", ("", "")))
    #foods.insert(0, (actual_nutritional_record['food']['id'],
                    #(actual_nutritional_record['food']['name'], actual_nutritional_record['food']['carbohydrates'])))
    form.food.choices = foods

    actual_nutritional_record['time'] = datetime.strptime(actual_nutritional_record['time'], '%H:%M:%S')
    actual_nutritional_record['time'] = actual_nutritional_record['time'].strftime('%H:%M')
    print(actual_nutritional_record['time'])

    if form.validate_on_submit():
        if form.amount_food.data == "" and form.food.data != None:
            flash('Si selecciona un alimento, debe espedificar su cantidad.', 'danger')
            return render_template('/update_nutritional_record.html', nutritional_records=nutritional_records,
                                   actual_nutritional_record=actual_nutritional_record, form=form)
        elif form.amount_food.data != "" and form.food.data == None:
            flash('Si especifica una cantidad, debe seleccionar un alimento.', 'danger')
            return render_template('/update_nutritional_record.html', nutritional_records=nutritional_records,
                                   actual_nutritional_record=actual_nutritional_record, form=form)
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
            if actual_nutritional_record["id"] == nutritional_records[-1]["id"]:
                data = {"diabetic_id": current_user.id}
                r = requests.get(
                    current_app.config["API_URL"] + '/suggestion',
                    headers=headers,
                    data=json.dumps(data))
                flash(json.loads(r.text), 'warning')
            return redirect(url_for('main.main_diabetic'))
        else:
            flash('No se pudo modificar el registro nutricional', 'danger')
    return render_template('/update_nutritional_record.html', nutritional_records=nutritional_records,
                           actual_nutritional_record=actual_nutritional_record, form=form)


@nutritional_record.route('/delete_nutritional_record/<int:nutritional_record_id>', methods=["DELETE", "GET"])
@token_vencido
@diabetic_required
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