from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

#importar las vistas
from src.views.persona_usuario_view import persona_usuario_view
app.register_blueprint(persona_usuario_view)

with app.app_context():
    db.create_all()