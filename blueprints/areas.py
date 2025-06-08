from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils import get_paginated_data
from db_queries import (
    obtener_detalles_version_recinto, # Para el contexto al crear una zona
    obtener_detalles_zona,
    guardar_nueva_zona,         # Anteriormente guardar_zona
    actualizar_zona,            # Anteriormente editar_zona
    obtener_svg_recinto_por_zona,
    obtener_secciones_listado,  # Para la tabla de secciones en detalle_zona
    obtener_total_secciones     # Para la tabla de secciones en detalle_zona
)

areas_bp = Blueprint(
    'areas',
    __name__,
    template_folder='../templates/theater_areas',
    url_prefix='/zonas' # o '/areas' si prefieres
)

# Ruta para mostrar el formulario de creación de zona
@areas_bp.route('/crear/para-version/<int:id_version>')
def crear_zona_form_route(id_version): # Ruta de app.py para crear_zona
    detalles_version = obtener_detalles_version_recinto(id_version)
    if not detalles_version:
        flash("Versión de recinto no encontrada para crear zona.", "error")
        return redirect(url_for('theater.index')) # O a una página de error o lista de versiones
    return render_template(
        "form_create_theater_area.html",
        detalles_recinto=detalles_version # La plantilla espera 'detalles_recinto'
    )

@areas_bp.route('/guardar/para-version/<int:id_version>', methods=['POST'])
def guardar_zona_route(id_version): # Ruta de app.py para guardar_zona
    try:
        nombre_zona = request.form["nombre_zona"]
        color_zona = request.form["area_color"]
        flash("Nueva zona guardada exitosamente", "success")
        guardar_nueva_zona(id_version, nombre_zona, color_zona)
        # Redirige de vuelta al formulario de creación de zona para la misma versión
        return redirect(url_for('areas.crear_zona_form_route', id_version=id_version))
    except KeyError as e:
        flash(f"Error al guardar nueva zona: Falta el campo {str(e)}", "error")
        return redirect(url_for('areas.crear_zona_form_route', id_version=id_version))
    except Exception as e:
        flash(f"Error inesperado al guardar nueva zona: {str(e)}", "error")
        return redirect(url_for('areas.crear_zona_form_route', id_version=id_version))

@areas_bp.route('/detalle/<int:id_zona>')
def detalle_zona_route(id_zona): # Ruta de app.py para detalle_zonas
    detalles_zona_data = obtener_detalles_zona(id_zona)
    if not detalles_zona_data:
        flash("Zona no encontrada.", "error")
        return redirect(url_for('theater.index')) # O a la lista de versiones/recintos

    svg_recinto_data = obtener_svg_recinto_por_zona(id_zona)
    secciones, pagination_obj = get_paginated_data(
        10, obtener_secciones_listado, obtener_total_secciones, id_zona
    )
    data_secciones = {"secciones": secciones, "pagination": pagination_obj}
    return render_template(
        "config_theater_areas.html",
        detalles_zona=detalles_zona_data,
        svg_recinto_por_zona=svg_recinto_data,
        data=data_secciones # La plantilla espera 'data' para las secciones
    )

@areas_bp.route('/editar/<int:id_zona>', methods=['POST'])
def editar_zona_route(id_zona): # Ruta de app.py para editar_zona
    detalles_zona_orig = obtener_detalles_zona(id_zona)
    if not detalles_zona_orig:
        flash("Zona no encontrada", "error")
        # Debería redirigir a una página apropiada, ej. detalle de la versión del recinto
        return redirect(url_for("theater.index")) # Placeholder

    # El método es POST
    nuevo_nombre = request.form["edit_area_name"]
    nuevo_color = request.form["edit_area_color"]
    # El input checkbox si no está marcado no se envía en el form.
    # request.form.get('edit_status', False) no funciona bien con 'true'/'false' o 'on'
    # Es mejor verificar la presencia de la clave
    nuevo_estatus_str = request.form.get("edit_status_hidden", "") # Usar el campo hidden
    nuevo_estatus = nuevo_estatus_str == 'true' if nuevo_estatus_str else False


    # Compara con el valor original de la base de datos
    # El valor de estatus_zona en la BD es booleano
    if (
        nuevo_nombre != detalles_zona_orig.get("nombre_zona")
        or nuevo_color != detalles_zona_orig.get("color_zona")
        or nuevo_estatus != detalles_zona_orig.get("estatus_zona")
    ):
        actualizar_zona(id_zona, nuevo_nombre, nuevo_color, nuevo_estatus)
        flash("Zona actualizada correctamente", "success")
    else:
        flash("No se realizaron cambios en la zona", "warning")
    return redirect(url_for("areas.detalle_zona_route", id_zona=id_zona))