# - *- coding: utf- 8 - *-
from flask_wtf import FlaskForm #Importa funciones de formulario
from wtforms import PasswordField, SubmitField, StringField, SelectField, HiddenField, IntegerField  # Importa campos
from wtforms.fields import EmailField,DateField, TimeField #Importa campos HTML
from wtforms import validators #Importa validaciones
from flask_login import current_user

class NutritionalRecordForm(FlaskForm):

    date = DateField('Introduzca la fecha:')

    time = TimeField('Introduzca la hora:')

    food = SelectField('Introduzca el alimento ingerido:',  coerce=int, validate_choice=False)

    glucose_value = IntegerField('Introduzca su valor glucémico:',
                            [
                                validators.data_required(message="Debe introducir su valor de glucosa"),
                                # validators.Required(message="Formato inválido")
                            ])





    submit = SubmitField('register')
