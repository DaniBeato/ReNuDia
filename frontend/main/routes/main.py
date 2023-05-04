from flask import Blueprint, render_template, current_app
import requests, json



main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
def nutritional_record():
    headers = {
        'content-type': "application/json",
        #'authorization': "Bearer {}".format(auth)
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


@main.route('/register')
def register():
    return render_template('/register.html')

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