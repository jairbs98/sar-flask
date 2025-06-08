# app.py
import flask
from utils import inject_global_variables # Usar importación relativa si app.py está al mismo nivel que utils.py
from config import config_by_name
import os
# from flask_wtf.csrf import CSRFProtect # Descomentar si implementas CSRF

# csrf = CSRFProtect() # Descomentar

# Importa tus blueprints
from main.routes import main_bp
from theater.routes import theater_bp
from versions.routes import versions_bp
from areas.routes import areas_bp
from sections.routes import sections_bp

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = flask.Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # csrf.init_app(app) # Descomentar para CSRF

    app.context_processor(inject_global_variables)

    # Registrar Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(theater_bp)
    app.register_blueprint(versions_bp)
    app.register_blueprint(areas_bp)
    app.register_blueprint(sections_bp)

    # (Opcional) Páginas de error personalizadas
    @app.errorhandler(404)
    def not_found_error(error):
        # app.logger.warning(f"Recurso no encontrado: {request.path} - {error}") # Necesitas importar request y app.logger (current_app)
        return flask.render_template('errors/404.html'), 404 # Asume que creas esta plantilla

    @app.errorhandler(500)
    def internal_error(error):
        # app.logger.error(f"Error interno del servidor: {error}", exc_info=True)
        return flask.render_template('errors/500.html'), 500 # Asume que creas esta plantilla

    return app

# Para ejecución local y para Gunicorn/WSGI
if __name__ == '__main__':
    flask_env = os.getenv('FLASK_ENV', 'dev')
    app = create_app(flask_env)
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
else: # Cuando es importado por Gunicorn u otro servidor WSGI
    # Gunicorn buscará una instancia de 'app' o llamará a create_app() si se especifica.
    # Si tu CMD de Docker es "gunicorn ... app:create_app()" no necesitas esto.
    # Si es "gunicorn ... app:app", entonces necesitas:
    gunicorn_app = create_app(os.getenv('FLASK_ENV', 'prod'))