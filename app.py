# app.py
import flask
from utils import (
    inject_global_variables,
)  # Usar importación relativa si app.py está al mismo nivel que utils.py
from config import config_by_name
import os
import bleach
from markupsafe import Markup

from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

from main.routes import main_bp
from theater.routes import theater_bp
from versions.routes import versions_bp
from areas.routes import areas_bp
from sections.routes import sections_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "default")

    app = flask.Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    csrf.init_app(app)

    app.context_processor(inject_global_variables)

    @app.template_filter("safe_html")
    def safe_html_filter(s):
        iframe_tags = ["iframe"]
        iframe_attrs = {
            "iframe": [
                "src",
                "width",
                "height",
                "style",
                "frameborder",
                "allowfullscreen",
                "loading",
                "referrerpolicy",
            ]
        }

        svg_tags = [
            "svg",
            "g",
            "path",
            "rect",
            "circle",
            "line",
            "polygon",
            "polyline",
            "text",
            "tspan",
            "defs",
            "use",
            "symbol",
            "style",
            "clipPath",
            "filter",
            "feGaussianBlur",
            "feOffset",
            "feColorMatrix",
        ]

        svg_attrs = {
            "*": ["class", "id", "style", "fill", "stroke", "stroke-width"],
            "svg": [
                "width",
                "height",
                "viewBox",
                "xmlns",
                "version",
                "preserveAspectRatio",
            ],
            "g": ["transform"],
            "path": ["d", "transform"],
            "rect": ["x", "y", "width", "height", "rx", "ry", "transform"],
            "circle": ["cx", "cy", "r", "transform"],
            "line": ["x1", "y1", "x2", "y2", "transform"],
            "polygon": ["points", "transform"],
            "polyline": ["points", "transform"],
            "text": [
                "x",
                "y",
                "dx",
                "dy",
                "text-anchor",
                "transform",
                "font-family",
                "font-size",
            ],
            "use": ["href", "x", "y", "width", "height"],
        }

        # Combinamos las listas de permitidos
        allowed_tags = iframe_tags + svg_tags
        # Combinamos los diccionarios de atributos
        allowed_attrs = {**iframe_attrs, **svg_attrs}

        # Limpiamos el HTML usando la lista combinada
        cleaned_html = bleach.clean(s, tags=allowed_tags, attributes=allowed_attrs)
        return Markup(cleaned_html)

    app.register_blueprint(main_bp)
    app.register_blueprint(theater_bp)
    app.register_blueprint(versions_bp)
    app.register_blueprint(areas_bp)
    app.register_blueprint(sections_bp)

    @app.errorhandler(404)
    def not_found_error(error):
        # app.logger.warning(f"Recurso no encontrado: {request.path} - {error}") # Necesitas importar request y app.logger (current_app)
        return (
            flask.render_template("errors/404.html"),
            404,
        )

    @app.errorhandler(500)
    def internal_error(error):
        # app.logger.error(f"Error interno del servidor: {error}", exc_info=True)
        return (
            flask.render_template("errors/500.html"),
            500,
        )

    return app


if __name__ == "__main__":
    flask_env = os.getenv("FLASK_ENV", "dev")
    app = create_app(flask_env)
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
else:
    gunicorn_app = create_app(os.getenv("FLASK_ENV", "prod"))
