from flask import render_template, Blueprint, redirect, request, url_for
from src.models.persona import Persona, Sexo
from src.models.usuario import Usuario
from src import db

persona_usuario_view = Blueprint('persona_usuario_view', __name__)

@persona_usuario_view.route('/', methods=['GET'])
def index():
    personas = db.session.query(Persona).join(Usuario).all()
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

@persona_usuario_view.route('/eliminar_persona/<int:id_persona>', methods=['POST'])
def eliminar_persona(id_persona):
    try:
        persona = db.session.query(Persona).filter_by(id_persona=id_persona).first()
        if persona:
            # Eliminar usuarios asociados antes de eliminar la persona
            db.session.query(Usuario).filter_by(id_persona=id_persona).delete()

            # Ahora eliminar la persona
            db.session.delete(persona)
            db.session.commit()
            
        return redirect(url_for('persona_usuario_view.index'))
    except Exception as e:
        db.session.rollback()  # En caso de error, hacer rollback
        return str(e)
