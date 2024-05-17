import os
from dotenv import load_dotenv
from pathlib import Path


base_dir = Path(__file__).resolve().parent

env_file = base_dir / '.env'

load_dotenv(env_file)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRED_MINUTES = 120
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'nowekontoprobne@gmail.com' 
    MAIL_PASSWORD ='jhweawsixqbzoxlp' 
    MAIL_DEFAULT_SENDER = 'nowekontoprobne@gmail.com' 
    # CELERY_BROKER_URL = 'redis://localhost:5000'
    # CELERY_RESULT_BACKEND = 'redis://localhost:5000'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI' )


class TestingConfig(Config):
    DB_FILE_PATH = base_dir / 'tests' / 'test.db'
    # SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_FILE_PATH}'
    # DB_FILE_PATH = Path(__file__).resolve().parent / 'tests' / 'test.db'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DB_HOST = os.environ.get('DB_HOST')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    MAIL_USERNAME = 'nowekontoprobne@gmail.com' 
    MAIL_PASSWORD ='jhweawsixqbzoxlp' 
    MAIL_DEFAULT_SENDER = 'nowekontoprobne@gmail.com' 


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
