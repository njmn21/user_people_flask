from flask import render_template, Blueprint, redirect, request, url_for
from src.models.persona import Persona, Sexo
from src.models.usuario import Usuario
from src import db

persona_usuario_view = Blueprint('persona_usuario_view', __name__)

@persona_usuario_view.route('/', methods=['GET'])
def index():
    personas = Persona.query.all()
    return render_template('index.html', personas=personas)

@persona_usuario_view.route('/registro')
def registro():
    return render_template('registro.html')

@persona_usuario_view.route('/registro_persona', methods=['POST'])
def registro_persona():
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
        rol = request.form['rol']

        sexo_enum = Sexo[sexo.upper()]

        nueva_persona = Persona(
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            dni=dni,
            telefono=telefono,
            sexo=sexo_enum,
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
        return str(e)

@persona_usuario_view.route('/editar_persona/<int:id>', methods=['GET', 'POST'])
def editar_persona(id):
    persona = Persona.query.get_or_404(id)
    if request.method == 'POST':
        try:
            persona.nombre = request.form['nombre']
            persona.apellido_paterno = request.form['apellido_paterno']
            persona.apellido_materno = request.form['apellido_materno']
            persona.dni = request.form['dni']
            persona.telefono = request.form['telefono']
            persona.sexo = Sexo[request.form['sexo'].upper()]
            persona.fecha_nacimiento = request.form['fecha_nacimiento']
            persona.correo = request.form['correo']
            persona.contrasenia = request.form['contrasenia']
            db.session.commit()
            return redirect(url_for('persona_usuario_view.index'))
        except Exception as e:
            return str(e)
    return render_template('editar_persona.html', persona=persona)

@persona_usuario_view.route('/eliminar_persona/<int:id>', methods=['POST'])
def eliminar_persona(id):
    try:
        persona = Persona.query.get_or_404(id)
        db.session.delete(persona)
        db.session.commit()
        return redirect(url_for('persona_usuario_view.index'))
    except Exception as e:
        return str(e)