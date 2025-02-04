import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = True

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{os.getenv('DATABASE_PASSWORD')}@localhost:3306/discoteca2'

class DevelopmentConfig(Config):
    DEBUG = True