from src import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_persona = db.Column(db.Integer, db.ForeignKey('personas.id_persona'), nullable=False)
    rol = db.Column(db.String(50), nullable=False)

    persona = db.relationship('Persona', back_populates='usuarios', lazy=True)

    def __init__(self, id_persona, rol):
        self.id_persona = id_persona
        self.rol = rol