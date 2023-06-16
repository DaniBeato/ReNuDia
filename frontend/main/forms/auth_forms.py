# - *- coding: utf- 8 - *-
from flask_wtf import FlaskForm #Importa funciones de formulario
from wtforms import PasswordField, SubmitField, StringField, SelectField, HiddenField, IntegerField  # Importa campos
from wtforms.fields import EmailField,DateField #Importa campos HTML
from wtforms import validators #Importa validaciones
from flask_login import current_user


class PreRegisterForm(FlaskForm):

    rol = SelectField('rol')

    submit = SubmitField('Registrarse')



class DiabeticRegisterForm(FlaskForm):

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

    gender = SelectField('gender')


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


    submit = SubmitField('Registrarse')




class NutritionistRegisterForm(FlaskForm):

        name = StringField('Ingrese su nombre: ',
                            [
                                validators.data_required(message = 'Debe introducir un nombre'),
                                validators.Length(min=2)
                            ])

        surname = StringField('Ingrese su apellido:',
                            [
                                validators.data_required(message='Debe introducir un apellido'),
                                validators.Length(min=5)
                            ])

        age = IntegerField('Ingrese su edad: ',
                            [
                                validators.data_required(message="Debe introducir su edad"),
                                #validators.Required(message="Formato inválido")
                            ])

        gender = SelectField('Ingrese su sexo:',validators=[validators.AnyOf(values=['Masculino', 'Femenino'])])


        doctor_license = StringField('Ingrese su número certificado profesional:',
                                    [
                                        validators.data_required(message="Debe introducir su número de certificado"),
                                        # validators.Required(message="Formato inválido")
                                    ])

        id_card = StringField('Ingrese su número de documento:',
                                     [
                                         validators.data_required(message="Debe introducir su número de documento"),
                                         # validators.Required(message="Formato inválido")
                                     ])

        email = EmailField('Ingrese su email:',
                           [
                               validators.data_required(message="Debe introducir su email"),
                               validators.Email(message='Formato inválido'),
                           ])

        password = PasswordField('Ingrese su contraseña:',
                                 [
                                     validators.data_required(message='Debe introducir su contraseña'),
                                     validators.Length(min=3)
                                 ])

        # rol = SelectField('Rol')

        submit = SubmitField('Registrarse')




class LoginForm(FlaskForm):
    email = EmailField('Ingrese su email:',
                       [
                           validators.data_required(message="Debe introducir su email"),
                           validators.Email(message='Formato inválido'),
                       ])

    password = PasswordField('Ingrese password:',
                             [
                                 validators.data_required(message='Debe introducir su contraseña'),
                                 validators.Length(min=3)
                             ])


    submit = SubmitField('login')



