from flask import render_template, Blueprint, redirect, request, url_for
from src.models.persona import Persona, Sexo
from src.models.usuario import Usuario
from src import db

persona_usuario_view = Blueprint('persona_usuario_view', __name__)

#inicio
@persona_usuario_view.route('/', methods=['GET'])
def index():
    personas = db.session.query(Persona).join(Usuario).all()
    return render_template('index.html', personas=personas)

#vista de registro
@persona_usuario_view.route('/registro', methods=['GET'])
def registro():
    id_persona = request.args.get('id_persona')
    persona = None
    if id_persona:
        persona = db.session.query(Persona).filter_by(id_persona=id_persona).first()
    return render_template('registro.html', persona=persona)

#accion de registro
@persona_usuario_view.route('/registro_persona', methods=['POST'])
def registro_persona():
    try:
        id_persona = request.form.get('id_persona')
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        dni = request.form['dni']
        telefono = request.form['telefono']
        sexo = request.form['sexo']
        fecha_nacimiento = request.form['fecha_nacimiento']
        correo = request.form['correo']
        contrasenia = request.form['contrasenia']
        rol = request.form['rol']

        if id_persona:
            persona = db.session.query(Persona).filter_by(id_persona=id_persona).first()
            if persona:
                persona.nombre = nombre
                persona.apellido_paterno = apellido_paterno
                persona.apellido_materno = apellido_materno
                persona.dni = dni
                persona.telefono = telefono
                persona.sexo = sexo
                persona.fecha_nacimiento = fecha_nacimiento
                persona.correo = correo
                persona.contrasenia = contrasenia
                persona.usuarios[0].rol = rol
        else:
            nueva_persona = Persona(
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                dni=dni,
                telefono=telefono,
                sexo=sexo,
                fecha_nacimiento=fecha_nacimiento,
                correo=correo,
                contrasenia=contrasenia
            )
            db.session.add(nueva_persona)
            db.session.flush()

            nuevo_usuario = Usuario(
                id_persona=nueva_persona.id_persona,
                rol=rol
            )
            db.session.add(nuevo_usuario)

        db.session.commit()
        return redirect(url_for('persona_usuario_view.index'))

    except Exception as e:
        db.session.rollback()
        return str(e)

#vista de registro de cliente
@persona_usuario_view.route('/registro_cliente', methods=['GET'])
def registro_cliente():
    return render_template('registro_cliente.html')

#accion de registro de cliente
@persona_usuario_view.route('/registro_persona_cliente', methods=['POST'])
def registro_persona_cliente():
    try:
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        dni = request.form['dni']
        telefono = request.form['telefono']
        sexo = request.form['sexo']
        fecha_nacimiento = request.form['fecha_nacimiento']
        correo = request.form['correo']
        contrasenia = request.form['contrasenia']

        nueva_persona = Persona(
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            dni=dni,
            telefono=telefono,
            sexo=sexo,
            fecha_nacimiento=fecha_nacimiento,
            correo=correo,
            contrasenia=contrasenia
        )
        db.session.add(nueva_persona)
        db.session.flush()

        nuevo_usuario = Usuario(
            id_persona=nueva_persona.id_persona,
            rol='Cliente'
        )
        db.session.add(nuevo_usuario)

        db.session.commit()
        return redirect(url_for('persona_usuario_view.index'))

    except Exception as e:
        db.session.rollback()
        return str(e)

#accion de eliminar
@persona_usuario_view.route('/eliminar_persona/<int:id_persona>', methods=['POST'])
def eliminar_persona(id_persona):
    try:
        persona = db.session.query(Persona).filter_by(id_persona=id_persona).first()
        if persona:
            db.session.query(Usuario).filter_by(id_persona=id_persona).delete()
            
            db.session.delete(persona)
            db.session.commit()
            
        return redirect(url_for('persona_usuario_view.index'))
    except Exception as e:
        db.session.rollback()
        return str(e)