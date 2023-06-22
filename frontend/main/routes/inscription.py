from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request
import requests, json
from .auth import token_vencido, nutritionist_required, diabetic_required
from flask_login import current_user

inscription = Blueprint('inscription', __name__, url_prefix='/inscription')


@inscription.route('/add_diabetic_to_nutritionist/<int:diabetic_id>', methods=['POST', "GET"])
@token_vencido
@nutritionist_required
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


@inscription.route('/inscriptions_of_nutritionist_list', methods=['POST', "GET"])
@token_vencido
@nutritionist_required
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
                           inscriptions_of_nutritionist=inscriptions_of_nutritionist)




@inscription.route('/delete_inscriptions_of_nutritionist/<int:inscription_id>', methods=['POST', "GET"])
@token_vencido
@nutritionist_required
def delete_inscriptions_of_nutritionist(inscription_id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }

    r = requests.delete(
        current_app.config["API_URL"] + '/inscriptions/{}'.format(inscription_id),
        headers=headers,
    )
    print(r.text)
    if r.status_code == 200:
        flash('Paciente eliminado correctamente', 'success')
        return redirect(url_for('inscription.inscriptions_of_nutritionist_list'))
    else:
        flash('No se pudo eliminar al paciente', 'danger')
        return redirect(url_for('inscription.inscriptions_of_nutritionist_list'))