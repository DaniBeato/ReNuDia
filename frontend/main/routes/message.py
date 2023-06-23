from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request
import requests, json
from ..forms.message_forms import MessageForm
from .auth import token_vencido, nutritionist_required, diabetic_required
from datetime import datetime
from flask_login import current_user


message = Blueprint('message', __name__, url_prefix='/message')


@message.route('/messages_nutritionist/<int:receptor_id>', methods=['GET', 'POST'])
@token_vencido
@nutritionist_required
def messages_nutritionist(receptor_id):
    form = MessageForm()

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
    inscriptions = json.loads(r.text)
    if len(inscriptions) == 0:
        flash('No tiene ningún paciente', 'danger')
        return redirect(url_for('main.main_nutritionist'))


    diabetics = []
    for inscription in inscriptions:
        diabetics.append(inscription["user_diabetic"])

    receptor = {"id": 0, "name": "Mensajes", "surname": "Sin Leer"}


    if receptor_id != 0:
        for diabetic in diabetics:
            if diabetic["id"] == receptor_id:
                diabetics.remove(diabetic)
                diabetics.append({"id": 0, "name": "Mensajes", "surname": "Sin Leer"})
                receptor = diabetic
                break

        data = {}
        data["sender_id"] = current_user.id
        data["receptor_id"] = receptor_id


        r = requests.get(
            current_app.config["API_URL"] + '/all_chat',
            headers=headers,
            data=json.dumps(data)
        )
        messages = json.loads(r.text)
        data = {}
        data['read'] = True
        for message in messages:
            if message["receptor_id"] == current_user.id and message['read'] == False:
                r = requests.put(
                    current_app.config["API_URL"] + '/messages/{}'.format(message["id"]),
                    headers=headers,
                    data=json.dumps(data)
                )

        unread_messages_sender = []
    else:
        data = {}
        data["receptor_id"] = current_user.id


        r = requests.get(
            current_app.config["API_URL"] + '/messages',
            headers=headers,
            data=json.dumps(data)
        )
        messages = json.loads(r.text)
        messages_unread_sender = ''
        for message in messages:
            if message["receptor_id"] == current_user.id and message['read'] == False:
                if message["sender"]["name"] + " " + message["sender"]["surname"] not in messages_unread_sender:
                    messages_unread_sender += message["sender"]["name"] + " " + message["sender"]["surname"] + " - "

        if len(messages_unread_sender) == 0:
            flash('No tienes mensajes nuevos', 'success')
        else:
            flash('Tienes mensajes sin leer de: ' + messages_unread_sender, 'success')


    if form.validate_on_submit():
        data = {}
        data["sender_id"] = current_user.id
        data["receptor_id"] = receptor_id
        data["message"] = form.message.data
        data["date"] = datetime.now().date().strftime('%Y-%m-%d')
        data["time"] = datetime.now().time().strftime('%H:%M')
        data["read"] = False

        r = requests.post(
            current_app.config["API_URL"] + '/messages',
            headers=headers,
            data=json.dumps(data)
        )

        data = {}
        data["sender_id"] = current_user.id
        data["receptor_id"] = receptor_id

        r = requests.get(
            current_app.config["API_URL"] + '/all_chat',
            headers=headers,
            data=json.dumps(data)
        )
        messages = json.loads(r.text)
    return render_template('/messages_nutritionist.html', messages=messages, diabetics=diabetics, form=form, receptor=receptor)



@message.route('/messages_diabetic', methods=['GET', 'POST'])
@token_vencido
@diabetic_required
def messages_diabetic():
    form = MessageForm()

    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    data = {"diabetic_id": current_user.id}
    r = requests.get(
        current_app.config["API_URL"] + '/inscriptions',
        headers=headers,
        data=json.dumps(data)
    )
    inscriptions = json.loads(r.text)
    if len(inscriptions) == 0:
        flash('Todavía no tienes un nutricionista asignado', 'danger')
        return redirect(url_for('main.main_diabetic'))
    nutritionist = inscriptions[0]["user_nutritionist"]



    if form.validate_on_submit():
        data = {}
        data["sender_id"] = current_user.id
        data["receptor_id"] = nutritionist["id"]
        data["message"] = form.message.data
        data["date"] = datetime.now().date().strftime('%Y-%m-%d')
        data["time"] = datetime.now().time().strftime('%H:%M')
        data["read"] = False

        r = requests.post(
            current_app.config["API_URL"] + '/messages',
            headers=headers,
            data=json.dumps(data)
        )

    data = {}
    data["sender_id"] = current_user.id
    data["receptor_id"] = nutritionist["id"]

    r = requests.get(
        current_app.config["API_URL"] + '/all_chat',
        headers=headers,
        data=json.dumps(data)
    )
    messages = json.loads(r.text)


    new_messages = False
    data = {}
    data['read'] = True
    for message in messages:
        if message["receptor_id"] == current_user.id and message['read'] == False:
            r = requests.put(
                current_app.config["API_URL"] + '/messages/{}'.format(message["id"]),
                headers=headers,
                data=json.dumps(data)
            )
            new_messages = True
    print(data)
    if new_messages == True:
        flash('Tiene nuevos mensajes sin leer', 'success')
    else:
        flash('No tiene mensajes nuevos', 'success')


    return render_template('/messages_diabetic.html', messages=messages, form=form, nutritionist=nutritionist)