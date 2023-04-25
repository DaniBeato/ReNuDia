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
    return render_template('/main.html', objects=users,
                           url=url, ths_list=ths_list, url_actual=url_actual)
    #return redirect(url_for('bolson.bolsones_en_venta'))
    #return render_template('/main/Vista_principal(1).html'

