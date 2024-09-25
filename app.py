import flask
from utils import inject_global_variables
from routes import *

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = 'CLAVE_SECRETA'

app.context_processor(inject_global_variables)
app.route('/')(home)
app.route('/recintos')(index)
app.route('/guardar', methods=['POST'])(guardar_recinto_principal)
app.route('/versiones_recinto/<int:recinto_id>')(versiones_recinto)
app.route('/crear_zona/<int:id_version>')(crear_zona)
app.route('/detalle_zonas/<int:id_zona>')(detalle_zonas)
app.route('/crear_seccion/<int:id_zona>')(crear_seccion)
app.route('/detalle_seccion/<int:id_seccion>')(detalle_seccion)
app.route('/detalle_recinto/<int:recinto_id>')(detalle_recinto)
app.route('/detalle_version_recinto/<int:version_id>')(detalle_version_recinto)
app.route('/guardar_version_recinto/<int:recinto_id>', methods=['POST'])(guardar_version_recinto)
app.route('/guardar_zona/<int:id_version>', methods=['POST'])(guardar_zona)
app.route('/guardar_seccion/<int:id_zona>', methods=['POST'])(guardar_seccion)
app.route('/editar_recinto/<int:recinto_id>', methods=['GET', 'POST'])(editar_recinto)
app.route('/editar_version_recinto/<int:version_id>', methods=['GET', 'POST'])(editar_version_recinto)
app.route('/editar_zona/<int:id_zona>', methods=['GET', 'POST'])(editar_zona)
app.route('/editar_detalle_seccion/<int:id_seccion>', methods=['GET', 'POST'])(editar_detalle_seccion)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
