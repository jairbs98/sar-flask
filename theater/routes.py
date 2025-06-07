from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_paginate import Pagination # Asegúrate que esta importación está aquí o en utils
from utils import get_paginated_data
from db_queries import (
    obtener_recintos_listado,
    obtener_total_recintos,
    guardar_recinto, # Anteriormente guardar_recinto_principal
    obtener_detalles_recinto,
    actualizar_recinto, # Anteriormente editar_recinto
    obtener_versiones_listado, # Para la tabla de versiones en detalle_recinto
    obtener_total_versiones   # Para la tabla de versiones en detalle_recinto
)

theater_bp = Blueprint(
    'theater',
    __name__,
    template_folder='../templates/theater', # Apunta a templates/theater/
    url_prefix='/recintos'
)

# Ruta original de theater/routes.py
@theater_bp.route('/')
def index(): # Esta era la función index de theater/routes.py
    page = request.args.get('page', 1, type=int)
    # Mueve la lógica de paginación aquí si no usas get_paginated_data
    # o asegúrate que get_paginated_data esté disponible.
    # El archivo routes.py original usaba per_page=10
    # El archivo routes.py global (que estamos refactorizando) usaba per_page=5 para esta ruta
    per_page = 5 # Ajusta según necesidad, o tómalo de config
    recintos, pagination_obj = get_paginated_data(
        per_page, obtener_recintos_listado, obtener_total_recintos
    )
    pag = {"recintos": recintos, "pagination": pagination_obj}
    return render_template('theaters.html', pag=pag) # buscará templates/theater/theaters.html

@theater_bp.route('/guardar', methods=['POST'])
def guardar_recinto_route(): # Ruta de app.py para guardar_recinto_principal
    try:
        name = request.form["name"]
        address = request.form["address"]
        map_data = request.form["map"] # Renombrado 'map' para evitar conflicto
        flash("Recinto guardado exitosamente", "success")
        guardar_recinto(name, address, map_data) # Llama a la función de db_queries
        return redirect(url_for("theater.index"))
    except KeyError as e:
        flash(f"Error al guardar: Falta el campo {str(e)}", "error")
    except Exception as e:
        flash(f"Error inesperado al guardar: {str(e)}", "error")
    return redirect(url_for("theater.index"))

@theater_bp.route('/detalle/<int:recinto_id>')
def detalle_recinto_route(recinto_id): # Ruta de app.py para detalle_recinto
    detalles_recinto_data = obtener_detalles_recinto(recinto_id)
    if not detalles_recinto_data:
        flash("Recinto no encontrado.", "error")
        return redirect(url_for('theater.index'))

    versiones, pagination_obj = get_paginated_data(
        10, obtener_versiones_listado, obtener_total_versiones, recinto_id
    )
    pag_v = {"versiones": versiones, "pagination": pagination_obj}
    return render_template(
        "config_theater.html", # buscará templates/theater/config_theater.html
        detalles_recinto=detalles_recinto_data,
        pag_v=pag_v
    )

@theater_bp.route('/editar/<int:recinto_id>', methods=['POST']) # Solo POST para la acción de editar
def editar_recinto_route(recinto_id): # Ruta de app.py para editar_recinto
    # La vista GET para el formulario de edición está en detalle_recinto_route
    # ya que el formulario está incrustado en config_theater.html
    detalles_recinto_orig = obtener_detalles_recinto(recinto_id)
    if detalles_recinto_orig is None:
        flash("Recinto no encontrado", "error")
        return redirect(url_for("theater.index"))

    # El método es POST por la definición de la ruta
    nuevo_nombre = request.form["edit_name"]
    nueva_direccion = request.form["edit_address"]
    nuevo_mapa = request.form["add_map"]

    if (
        nuevo_nombre != detalles_recinto_orig["nombre"]
        or nueva_direccion != detalles_recinto_orig["direccion"]
        or nuevo_mapa != detalles_recinto_orig["mapa"]
    ):
        actualizar_recinto(recinto_id, nuevo_nombre, nueva_direccion, nuevo_mapa)
        flash("Actualizado correctamente", "success")
    else:
        flash("No se realizaron cambios", "warning")
    return redirect(url_for("theater.detalle_recinto_route", recinto_id=recinto_id))