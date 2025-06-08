from flask import Blueprint, render_template
# Si 'home' necesita datos de db_queries o utils, impórtalos con 'from .. import'
# from ..db_queries import alguna_funcion_si_es_necesaria

main_bp = Blueprint(
    'main',
    __name__,
    template_folder='../templates' # Apunta a la carpeta raíz de plantillas
)

@main_bp.route('/')
def home():
    return render_template('theater/home.html')