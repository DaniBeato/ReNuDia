# - *- coding: utf- 8 - *-
from flask_wtf import FlaskForm #Importa funciones de formulario
from wtforms import PasswordField, SubmitField, StringField, SelectField, HiddenField, IntegerField  # Importa campos
from wtforms.fields import EmailField,DateField, TimeField #Importa campos HTML
from wtforms import validators #Importa validaciones
from flask_login import current_user

class MessageForm(FlaskForm):

    message = StringField('Escriba su mensaje aquí:')


    submit = SubmitField('Enviar')


class MessageFilter(FlaskForm):
    diabetic = SelectField('Paciente Diabético',[validators.optional()], coerce=int)
    submit = SubmitField("Ver mensajes")


