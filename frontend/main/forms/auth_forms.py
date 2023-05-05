# - *- coding: utf- 8 - *-
from flask_wtf import FlaskForm #Importa funciones de formulario
from wtforms import PasswordField, SubmitField, StringField, SelectField, HiddenField, IntegerField  # Importa campos
from wtforms.fields import EmailField,DateField #Importa campos HTML
from wtforms import validators #Importa validaciones
from flask_login import current_user

class RegisterForm(FlaskForm):

    name = StringField('name',
                         [
                             validators.data_required(message = 'Debe introducir un nombre'),
                             validators.Length(min=2)
                         ])

    surname = StringField('surname',
                        [
                             validators.data_required(message='Debe introducir un apellido'),
                             validators.Length(min=5)
                        ])



    age = IntegerField('age',
                        [
                         validators.data_required(message="Debe introducir su edad"),
                         #validators.Required(message="Formato inválido")
                        ])

    weight = IntegerField('weight',
                       [
                           validators.data_required(message="Debe introducir su peso"),
                           # validators.Required(message="Formato inválido")
                       ])


    height = IntegerField('height',
                          [
                                validators.data_required(message="Debe introducir su altura"),
                                # validators.Required(message="Formato inválido")
                            ])

    gender = StringField('gender',
                       [
                           validators.data_required(message="Debe introducir su sexo"),
                           # validators.Required(message="Formato inválido")
                       ])


    diabetes_type = StringField('diabetes_type',
                          [
                                validators.data_required(message="Debe introducir su tipo de diabetes"),
                                # validators.Required(message="Formato inválido")
                            ])



    email = EmailField('email',
      [
          validators.data_required(message="Debe introducir su email"),
          validators.Email(message='Formato inválido'),
      ])


    password = PasswordField('password',
    [
        validators.data_required(message='Debe introducir su contraseña'),
        validators.Length(min=3)
    ])

    #rol = SelectField('Rol')


    submit = SubmitField('register')


class LoginForm(FlaskForm):
    email = EmailField('email',
                       [
                           validators.data_required(message="Debe introducir su email"),
                           validators.Email(message='Formato inválido'),
                       ])

    password = PasswordField('password',
                             [
                                 validators.data_required(message='Debe introducir su contraseña'),
                                 validators.Length(min=3)
                             ])


    submit = SubmitField('login')


