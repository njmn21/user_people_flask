from enum import Enum
from src import db

class Sexo(Enum):
    masculino = 'masculino'
    femenino = 'femenino'

class Persona(db.Model):
    __tablename__ = 'personas'

    id_persona = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido_paterno = db.Column(db.String(50), nullable=False)
    apellido_materno = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(8), nullable=False, unique=True)
    telefono = db.Column(db.String(15), nullable=False)
    sexo = db.Column(db.Enum(Sexo))
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    correo = db.Column(db.String(150), nullable=False, unique=True)
    contrasenia = db.Column(db.String(150), nullable=False)
    estado = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, server_default=db.func.now())

    usuarios = db.relationship('Usuario', back_populates='persona', lazy=True)

    def __init__(self, nombre, apellido_paterno, apellido_materno, 
                 dni, telefono, sexo, fecha_nacimiento, correo, contrasenia):
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.dni = dni
        self.telefono = telefono
        self.sexo = sexo
        self.fecha_nacimiento = fecha_nacimiento
        self.correo = correo
        self.contrasenia = contrasenia