from flask import flash,Blueprint, render_template, redirect, url_for, current_app, request
import requests, json
from .auth import admin_required, admin_or_proveedor_required, admin_or_cliente_required, token_vencido, cliente_required
from main.forms.usuario_forms import UsuarioForm
from main.forms.usuario_forms import UsuarioFilter
from main.forms.compra_forms import CompraForm
from main.forms.compra_forms import CompraFilter
from flask_login import current_user
from datetime import datetime
from .main import main





usuario = Blueprint('usuario', __name__, url_prefix = '/usuario')



@usuario.route('/administradores')
@token_vencido
@admin_required
def administradores():
    filter = UsuarioFilter(request.args, meta={'csrf': False})
    data = {}
    data['pagina'] = "1"
    data['cantidad_elementos'] = "5"
    if 'pagina' in request.args:
        # Si se han usado los botones de paginación cargar nueva página
        data["pagina"] = request.args.get('pagina', '')
    if filter.submit():
        if filter.nombre.data != '':
            data["nombre"] = filter.nombre.data
        if filter.apellido.data != '':
            data["apellido"] = filter.apellido.data
        print(filter.apellido.data)
    print(data)

    auth = request.cookies['token_acceso']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    # print(headers)

    r = requests.get(
        current_app.config["API_URL"] + '/administradores',
        headers=headers,
        data=json.dumps(data))

    print(r.text)
    administradores = json.loads(r.text)['Administradores']
    paginacion = {}
    paginacion["cantidad_paginas"] = json.loads(r.text)["Cantidad de páginas"]
    paginacion["pagina_actual"] = json.loads(r.text)["Página actual"]

    header = "Lista de Administradores"
    url = 'usuario.administrador'
    ths_list = ['nombre', 'apellido']
    url_actual = 'usuario.administradores'
    return render_template('/usuario/Administradores_lista(4).html', objects = administradores, header = header, url = url, ths_list = ths_list, first_dict = 0,
                           paginacion = paginacion, filter = filter,  url_actual = url_actual)



@usuario.route('/administrador/<int:id>')
@token_vencido
@admin_required
def administrador(id):
    auth = request.cookies['token_acceso']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    r = requests.get(
        current_app.config["API_URL"] + '/administrador/' + str(id),
        headers=headers)
    if (r.status_code == 404):
        return redirect(url_for('usuario.administradores'))
    administrador = json.loads(r.text)
    header = "Administrador"
    return render_template('/usuario/Administrador(5).html', object = administrador, header = header)



@usuario.route('/editar_administrador/<int:id>', methods=["GET", "PUT", "POST"])
@token_vencido
@admin_required
def editar_administrador(id):
    form = UsuarioForm()  # Instanciar formulario
    form.rol.choices = ["admin"]
    if form.validate_on_submit():  # Si el formulario ha sido enviado y es validado correctamente
        data = {}
        data["nombre"] = form.nombre.data
        data["apellido"] = form.apellido.data
        data["mail"] = form.email.data
        data['telefono'] = form.telefono.data
        data["contrasenia"] = form.contrasenia.data
        data["rol"] = form.rol.data
        print(data)
        auth = request.cookies['token_acceso']
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer {}".format(auth)
        }
        r = requests.put(
            current_app.config["API_URL"] + '/administrador/' + str(id),
            headers=headers,
            data=json.dumps(data))
        print(r.text)
        if r.status_code == 204:
            flash('Administrador actualizado.', 'warning')
            return redirect(url_for('usuario.administradores'))
        else:
            flash('Error.', 'warning')
            return redirect(url_for('usuario.administradores'))
    header = "Editar Administrador"
    auth = request.cookies['token_acceso']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    r = requests.get(
        current_app.config["API_URL"] + '/administrador/' + str(id),
        headers=headers)
    administrador = json.loads(r.text)
    print(administrador)
    url = 'usuario.editar_administrador'
    return render_template('/usuario/Editar_usuario(34).html', id=administrador['id'],
                           form=form, header=header, url = url)


@usuario.route('/eliminar_administrador/<int:id>')
@token_vencido
@admin_required
def eliminar_administrador(id):
    auth = request.cookies['token_acceso']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    adios = False
    if current_user.id == id:
        adios = True

    r = requests.delete(
        current_app.config["API_URL"] + '/administrador/' + str(id),
        headers=headers)
    if  r.status_code == 204:
        if adios:
            flash('Se ha eliminado su usuario.', 'warning')
            return redirect(url_for('main.cerrar_sesion'))
        else:
            flash('Administrador eliminado.', 'warning')
            return redirect(url_for('usuario.administradores'))
    else:
        flash('Error', 'warning')
        return redirect(url_for('usuario.administradores'))


@usuario.route('/clientes')
@token_vencido
@admin_required
def clientes():
    filter = UsuarioFilter(request.args, meta={'csrf': False})
    data = {}
    data['pagina'] = "1"
    data['cantidad_elementos'] = "5"
    if 'pagina' in request.args:
        # Si se han usado los botones de paginación cargar nueva página
        data["pagina"] = request.args.get('pagina', '')
    if filter.submit():
        if filter.nombre.data != '':
            data["nombre"] = filter.nombre.data
        if filter.apellido.data != '':
            data["apellido"] = filter.apellido.data
        print(filter.apellido.data)
    print(data)

    auth = request.cookies['token_acceso']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    # print(headers)

    r = requests.get(
        current_app.config["API_URL"] + '/clientes',
        headers=headers,
        data=json.dumps(data))

    print(r.text)
    paginacion = {}
    paginacion["cantidad_paginas"] = json.loads(r.text)["Cantidad de páginas"]
    paginacion["pagina_actual"] = json.loads(r.text)["Página actual"]


    clientes = json.loads(r.text)['Clientes']
    header = "Lista de Clientes"
    ths_list = ['nombre', 'apellido']
    url = 'usuario.cliente'
    url_actual = 'usuario.clientes'
    return render_template('/usuario/Clientes_lista(17).html', objects = clientes, header = header, ths_list = ths_list, url = url, first_dict = 0,
                           paginacion = paginacion, filter = filter, url_actual = url_actual)



@usuario.route('/cliente/<int:id>')
@token_vencido
@admin_or_cliente_required
def cliente(id):
    auth = request.cookies['token_acceso']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    r = requests.get(
        current_app.config["API_URL"] + '/cliente/' + str(id),
        headers=headers)
    if (r.status_code == 404):
        return redirect(url_for('usuario.clientes'))
    cliente = json.loads(r.text)
    header = 'Cliente'
    return render_template('/usuario/Cliente(18).html', object = cliente, header = header)



@usuario.route('/editar_cliente/<int:id>', methods=["GET", "PUT", "POST"])
@token_vencido
@admin_or_cliente_required
def editar_cliente(id):
    form = UsuarioForm()  # Instanciar formulario
    form.rol.choices = ["cliente"]
    if form.validate_on_submit():  # Si el formulario ha sido enviado y es validado correctamente
        data = {}
        data["nombre"] = form.nombre.data
        data["apellido"] = form.apellido.data
        data["mail"] = form.email.data
        data['telefono'] = form.telefono.data
        data["contrasenia"] = form.contrasenia.data
        data["rol"] = form.rol.data
        print(data)
        auth = request.cookies['token_acceso']
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer {}".format(auth)
        }
        r = requests.put(
            current_app.config["API_URL"] + '/cliente/' + str(id),
            headers=headers,
            data=json.dumps(data))
        print(r.text)
        if r.status_code == 204:
            flash('Cliente actualizado.', 'warning')
            return redirect(url_for('usuario.clientes'))
        else:
            flash('Error.', 'warning')
            return redirect(url_for('usuario.clientes'))
    header = "Editar Cliente"
    auth = request.cookies['token_acceso']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    r = requests.get(
        current_app.config["API_URL"] + '/cliente/' + str(id),
        headers=headers)
    cliente = json.loads(r.text)
    print(cliente)
    url = 'usuario.editar_cliente'
    return render_template('/usuario/Editar_usuario(34).html', id=cliente['id'],
                           form=form, header=header, url = url)


@usuario.route('/eliminar_cliente/<int:id>')
@token_vencido
@admin_or_cliente_required
def eliminar_cliente(id):
    auth = request.cookies['token_acceso']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    adios = False
    if current_user.id == id:
        adios = True
    r = requests.delete(
        current_app.config["API_URL"] + '/cliente/' + str(id),
        headers=headers)
    if r.status_code == 204:
        if adios:
            flash('Se ha eliminado su usuario.', 'warning')
            return redirect(url_for('main.cerrar_sesion'))
        else:
            flash('Cliente eliminado.', 'warning')
            return redirect(url_for('usuario.clientes'))
    else:
        flash('Error', 'warning')
        return redirect(url_for('usuario.clientes'))


@usuario.route('/compras')
@token_vencido
@admin_or_cliente_required
def compras():
    if current_user.rol == "admin":
        filter = CompraFilter(request.args, meta={'csrf': False})
        data = {}
        data['pagina'] = "1"
        data['cantidad_elementos'] = "5"
        if 'pagina' in request.args:
            # Si se han usado los botones de paginación cargar nueva página
            data["pagina"] = request.args.get('pagina', '')
        if filter.submit():
            if filter.usuario_ID.data != '' and filter.usuario_ID.data != None:
                data["usuario_ID"] = filter.usuario_ID.data
            if filter.retirado.data != '' and filter.retirado.data != None:
                if filter.retirado.data == str('No'):
                    data["retirado"] = 0
                else:
                    data["retirado"] = 1

        auth = request.cookies['token_acceso']
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer {}".format(auth)
        }
        # print(headers)

        r = requests.get(
            current_app.config["API_URL"] + '/compras',
            headers=headers,
            data=json.dumps(data))

        print(r.text)

        paginacion = {}
        paginacion["cantidad_paginas"] = json.loads(r.text)["Cantidad de páginas"]
        paginacion["pagina_actual"] = json.loads(r.text)["Página actual"]

        compras = json.loads(r.text)['Compras']
        print(compras)
        header = 'Lista de Compras'
        url = 'usuario.compra'
        ths_list = ['id','fecha_compra', 'retirado']
        url_actual = 'usuario.compras'
        return render_template('/usuario/Compras_lista(19).html', objects = compras, header = header, url = url, ths_list = ths_list, first_dict = 0,
                               paginacion = paginacion, filter = filter,  url_actual = url_actual)
    else:
        filter = CompraFilter(request.args, meta={'csrf': False})
        data = {}
        data['pagina'] = "1"
        data['cantidad_elementos'] = "5"
        data["usuario_ID"] = str(current_user.id)
        if 'pagina' in request.args:
            # Si se han usado los botones de paginación cargar nueva página
            data["pagina"] = request.args.get('pagina', '')
        if filter.submit():
            data["usuario_ID"] = str(current_user.id)
            if filter.retirado.data != '' and filter.retirado.data != None:
                if filter.retirado.data == str('No'):
                    data["retirado"] = 0
                else:
                    data["retirado"] = 1

        auth = request.cookies['token_acceso']
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer {}".format(auth)
        }
        # print(headers)

        r = requests.get(
            current_app.config["API_URL"] + '/compras',
            headers=headers,
            data=json.dumps(data))

        print(r.text)

        paginacion = {}
        paginacion["cantidad_paginas"] = json.loads(r.text)["Cantidad de páginas"]
        paginacion["pagina_actual"] = json.loads(r.text)["Página actual"]

        compras = json.loads(r.text)['Compras']
        print(compras)
        header = 'Lista de Compras'
        url = 'usuario.compra'
        ths_list = ['id', 'fecha_compra', 'retirado']
        url_actual = 'usuario.compras'
        return render_template('/usuario/Compras_lista(19).html', objects=compras, header=header, url=url,
                               ths_list=ths_list, first_dict=0,
                               paginacion=paginacion, filter=filter, url_actual=url_actual)



@usuario.route('/compra/<int:id>')
@token_vencido
@admin_or_cliente_required
def compra(id):
    auth = request.cookies['token_acceso']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    r = requests.get(
        current_app.config["API_URL"] + '/compra/' + str(id),
        headers=headers)
    if (r.status_code == 404):
        return redirect(url_for('usuario.compras'))
    compra = json.loads(r.text)
    header = 'Compra'
    return render_template('/usuario/Compra(20).html', object = compra, header = header)


@usuario.route('/crear_compra/<int:id>', methods=["GET", "PUT", "POST"])
@token_vencido
@admin_or_cliente_required
def crear_compra(id):
    auth = request.cookies['token_acceso']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }

    data = {}
    data['usuario_ID'] = str(current_user.id)
    data['bolsonID'] = str(id)
    data['retirado'] = 0
    data['fecha_compra'] = datetime.now().strftime('%d/%m/%Y')
    print('datos de compra', data)

    r = requests.post(
        current_app.config["API_URL"] + '/compras',
        headers=headers,
        data=json.dumps(data))
    print(r.text)
    if r.status_code == 204:
        flash('Compra creada.', 'warning')
        return redirect(url_for('bolson.bolsones_en_venta'))
    else:
        flash('Error.', 'warning')
        return redirect(url_for('bolson.bolsones_en_venta'))



@usuario.route('/editar_compra/<int:id>', methods=["GET", "PUT", "POST"])
@token_vencido
@admin_required
def editar_compra(id):
    form = CompraForm()  # Instanciar formulario
    if form.validate_on_submit():  # Si el formulario ha sido enviado y es validado correctamente
        data = {}
        data["usuario_ID"] = form.usuario_ID.data
        data["bolsonID"] = form.bolsonID.data
        data["retirado"] = form.retirado.data
        data['fecha_compra'] = form.fecha_compra.data.strftime('%d/%m/%Y')
        print(data)
        auth = request.cookies['token_acceso']
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer {}".format(auth)
        }
        r = requests.put(
            current_app.config["API_URL"] + '/compra/' + str(id),
            headers=headers,
            data=json.dumps(data))
        print(r.text)
        if r.status_code == 204:
            flash('Compra actualizada.', 'warning')
            return redirect(url_for('usuario.compras'))
        else:
            flash('Error.', 'warning')
            return redirect(url_for('usuario.compras'))
    header = "Editar Compra"
    auth = request.cookies['token_acceso']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    r = requests.get(
        current_app.config["API_URL"] + '/compra/' + str(id),
        headers=headers)
    compra = json.loads(r.text)
    print(compra)
    return render_template('/usuario/Editar_compra(35).html', id=compra['id'],
                           form=form, header=header)

@usuario.route('/eliminar_compra/<int:id>')
@token_vencido
@admin_required
def eliminar_compra(id):
    auth = request.cookies['token_acceso']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    r = requests.delete(
        current_app.config["API_URL"] + '/compra/' + str(id),
        headers=headers)
    if  r.status_code == 204:
        flash('Compra eliminada.', 'warning')
        return redirect(url_for('usuario.compras'))
    else:
        flash('Error', 'warning')
        return redirect(url_for('usuario.compras'))



@usuario.route('/proveedores')
@admin_required
def proveedores():
    filter = UsuarioFilter(request.args, meta={'csrf': False})
    data = {}
    data['pagina'] = "1"
    data['cantidad_elementos'] = "5"
    if 'pagina' in request.args:
        # Si se han usado los botones de paginación cargar nueva página
        data["pagina"] = request.args.get('pagina', '')
    if filter.submit():
        if filter.nombre.data != '':
            data["nombre"] = filter.nombre.data
        if filter.apellido.data != '':
            data["apellido"] = filter.apellido.data
        print(filter.apellido.data)
    print(data)

    auth = request.cookies['token_acceso']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    # print(headers)

    r = requests.get(
        current_app.config["API_URL"] + '/proveedores',
        headers=headers,
        data=json.dumps(data))
    print(r.text)

    paginacion = {}
    paginacion["cantidad_paginas"] = json.loads(r.text)["Cantidad de páginas"]
    paginacion["pagina_actual"] = json.loads(r.text)["Página actual"]

    proveedores = json.loads(r.text)['Proveedores']
    header = 'Lista de Proveedores'
    url = 'usuario.proveedor'
    ths_list = ['nombre', 'apellido']
    url_actual = 'usuario.proveedores'
    return render_template('/usuario/Proveedores_lista(23).html', objects = proveedores, header = header, url = url, ths_list = ths_list, first_dict = 0,
                           paginacion = paginacion, filter = filter, url_actual = url_actual)



@usuario.route('/proveedor/<int:id>')
@token_vencido
@admin_or_proveedor_required
def proveedor(id):
    auth = request.cookies['token_acceso']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    r = requests.get(
        current_app.config["API_URL"] + '/proveedor/' + str(id),
        headers=headers)
    if (r.status_code == 404):
        return redirect(url_for('usuario.proveedores'))
    proveedor = json.loads(r.text)
    header = 'Proveedor'
    return render_template('/usuario/Proveedor(24).html', object = proveedor, header = header)



@usuario.route('/editar_proveedor/<int:id>', methods=["GET", "PUT", "POST"])
@token_vencido
@admin_or_proveedor_required
def editar_proveedor(id):
    form = UsuarioForm()
    form.rol.choices = ["proveedor"]# Instanciar formulario
    if form.validate_on_submit():  # Si el formulario ha sido enviado y es validado correctamente
        data = {}
        data["nombre"] = form.nombre.data
        data["apellido"] = form.apellido.data
        data["mail"] = form.email.data
        data['telefono'] = form.telefono.data
        data["contrasenia"] = form.contrasenia.data
        data["rol"] = form.rol.data
        print(data)
        auth = request.cookies['token_acceso']
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer {}".format(auth)
        }
        r = requests.put(
            current_app.config["API_URL"] + '/proveedor/' + str(id),
            headers=headers,
            data=json.dumps(data))
        print(r.text)
        if r.status_code == 204:
            flash('Proveedor actualizado.', 'warning')
            return redirect(url_for('usuario.proveedores'))
        else:
            flash('Error.', 'warning')
            return redirect(url_for('usuario.proveedores'))
    header = "Editar Proveedor"
    auth = request.cookies['token_acceso']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    r = requests.get(
        current_app.config["API_URL"] + '/proveedor/' + str(id),
        headers=headers)
    proveedor = json.loads(r.text)
    print(proveedor)
    url = 'usuario.editar_proveedor'
    return render_template('/usuario/Editar_usuario(34).html', id=proveedor['id'],
                           form=form, header=header, url=url)


@usuario.route('/eliminar_proveedor/<int:id>')
@token_vencido
@admin_required
def eliminar_proveedor(id):
    auth = request.cookies['token_acceso']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer {}".format(auth)
    }
    adios = False
    if current_user.id == id:
        adios = True
    r = requests.delete(
        current_app.config["API_URL"] + '/proveedor/' + str(id),
        headers=headers)
    if r.status_code == 204:
        if adios:
            flash('Se ha eliminado su usuario.', 'warning')
            return redirect(url_for('main.cerrar_sesion'))
        else:
            flash('Proveedor eliminado.', 'warning.')
            return redirect(url_for('usuario.proveedores'))
    else:
        flash('Error', 'warning')
        return redirect(url_for('usuario.proveedores'))















