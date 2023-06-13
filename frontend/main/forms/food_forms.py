# - *- coding: utf- 8 - *-
from flask_wtf import FlaskForm #Importa funciones de formulario
from wtforms import PasswordField, SubmitField, StringField, SelectField, HiddenField, IntegerField, FloatField  # Importa campos
from wtforms.fields import EmailField,DateField, TimeField #Importa campos HTML
from wtforms import validators #Importa validaciones
from flask_login import current_user

class FoodForm(FlaskForm):

    name = StringField('Introduzca el nombre del alimento:')

    carbohydrates = FloatField('Introduzca la cantidad de carbohidratos que posee el alimento:')



    submit = SubmitField('Guardar')
