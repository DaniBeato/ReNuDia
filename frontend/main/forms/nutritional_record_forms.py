# - *- coding: utf- 8 - *-
from flask_wtf import FlaskForm #Importa funciones de formulario
from wtforms import PasswordField, SubmitField, StringField, SelectField, HiddenField, DateField, BooleanField, IntegerField #Importa campos
from wtforms.fields.html5 import EmailField, DateField #Importa campos HTML
from wtforms import validators #Importa validaciones

class NutritionalRecordForm(FlaskForm):

    date = DateField('Fecha')

    food_id = IntegerField('Id de alimento')


    user_id = IntegerField('Id de usuario')


    glucose_value = IntegerField('Cantidad de glucosa')





    submit = SubmitField('Guardar Información')

