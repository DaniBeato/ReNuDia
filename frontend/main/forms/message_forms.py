# - *- coding: utf- 8 - *-
from flask_wtf import FlaskForm #Importa funciones de formulario
from wtforms import PasswordField, SubmitField, StringField, SelectField, HiddenField, IntegerField  # Importa campos
from wtforms.fields import EmailField,DateField, TimeField #Importa campos HTML
from wtforms import validators #Importa validaciones
from flask_login import current_user

class MessageForm(FlaskForm):


    message = StringField('Escriba su mensaje aquí:', [
                           validators.data_required(message="Debe introducir un mensaje"),
                           # validators.Required(message="Formato inválido")
                       ])


    submit = SubmitField('Enviar Mensaje')





