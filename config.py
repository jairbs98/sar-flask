import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = False
    TESTING = False

    # Configuración de la Base de Datos
    DB_DRIVER = os.environ.get("DB_DRIVER")
    DB_HOSTNAME = os.environ.get("DB_HOSTNAME")
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_DATABASE = os.environ.get("DB_DATABASE")
    DB_PORT = os.environ.get("DB_PORT")


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""

    DEBUG = True


class ProductionConfig(Config):
    """Configuración para producción."""

    # En producción, DEBUG debería ser False por seguridad.
    # Se puede sobrescribir con una variable de entorno si es necesario.
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() == "true"


config_by_name = dict(
    dev=DevelopmentConfig, prod=ProductionConfig, default=DevelopmentConfig
)
