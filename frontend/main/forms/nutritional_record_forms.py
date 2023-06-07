# - *- coding: utf- 8 - *-
from flask_wtf import FlaskForm #Importa funciones de formulario
from wtforms import PasswordField, SubmitField, StringField, SelectField, HiddenField, IntegerField  # Importa campos
from wtforms.fields import EmailField,DateField, TimeField #Importa campos HTML
from wtforms import validators #Importa validaciones
from flask_login import current_user

class NutritionalRecordForm(FlaskForm):

    date = DateField('Introduzca la fecha:')

    time = TimeField('Introduzca la hora:')

    food = SelectField('Introduzca el alimento ingerido:', [validators.NoneOf([0], message="Debe seleccionar un alimento", values_formatter=None)], coerce=int, validate_choice=False)


    glucose_value = IntegerField('Introduzca su valor glucémico:',
                            [
                                validators.data_required(message="Debe introducir su valor de glucosa"),
                                # validators.Required(message="Formato inválido")
                            ])

    amount_food = StringField('Introduzca la cantidad del alimento que ha ingerido:',
                            [
                                validators.data_required(message="Debe introducir la cantidad del alimento que ha ingerido"),
                                # validators.Required(message="Formato inválido")
                            ])


    submit = SubmitField('Guardar')
