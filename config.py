# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-por-defecto-muy-segura' # Un valor por defecto es útil para desarrollo local
    DEBUG = False
    TESTING = False

    # Configuración de la Base de Datos
    DB_DRIVER = os.environ.get('DB_DRIVER', 'postgresql')
    DB_HOSTNAME = os.environ.get('DB_HOSTNAME', 'localhost')
    DB_USERNAME = os.environ.get('DB_USERNAME', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'admin')
    DB_DATABASE = os.environ.get('DB_DATABASE', 'svg')
    DB_PORT = os.environ.get('DB_PORT', '5432')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    # Puedes forzar DEBUG a False o tomarlo de una variable de entorno específica para producción
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    # Aquí podrías tener configuraciones de logging más robustas, etc.

config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig,
    default=DevelopmentConfig
)