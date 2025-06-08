from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils import get_paginated_data
from db_queries import (
    obtener_detalles_recinto, # Para el contexto al crear una versión
    obtener_detalles_version_recinto,
    guardar_nueva_version_recinto, # Anteriormente guardar_version_recinto
    actualizar_version_recinto,   # Anteriormente editar_version_recinto
    obtener_zonas_listado,      # Para la tabla de zonas en detalle_version
    obtener_total_zonas         # Para la tabla de zonas en detalle_version
)

versions_bp = Blueprint(
    'versions',
    __name__,
    template_folder='../templates/theater_versions',
    url_prefix='/versiones'
)

# Ruta para mostrar el formulario de creación de versión
@versions_bp.route('/crear/para-recinto/<int:recinto_id>')
def crear_version_form_route(recinto_id): # Ruta de app.py para versiones_recinto
    detalles_recinto_data = obtener_detalles_recinto(recinto_id)
    if not detalles_recinto_data:
        flash("Recinto no encontrado para crear versión.", "error")
        # Considera redirigir a una página más apropiada si 'theater.index' no es ideal
        return redirect(url_for('theater.index')) # Asumiendo que theater.index es el listado de recintos
    # version_recinto = obtener_versiones_recinto(recinto_id) # Esta variable no se usaba en la plantilla
    return render_template(
        "form_create_theater_version.html",
        detalles_recinto=detalles_recinto_data
        # version_recinto=version_recinto # Descomentar si se usa
    )

@versions_bp.route('/guardar/para-recinto/<int:recinto_id>', methods=['POST'])
def guardar_version_route(recinto_id): # Ruta de app.py para guardar_version_recinto
    try:
        nom_version = request.form["nom_version"]
        svg_recinto = request.files["svg_recinto"].read().decode("utf-8")
        flash("Nueva versión guardada exitosamente", "success")
        guardar_nueva_version_recinto(recinto_id, nom_version, svg_recinto)
        return redirect(url_for("theater.detalle_recinto_route", recinto_id=recinto_id))
    except KeyError as e:
        flash(f"Error al guardar nueva versión: Falta el campo {str(e)}", "error")
        # Es mejor redirigir al formulario de creación con el error
        return redirect(url_for("versions.crear_version_form_route", recinto_id=recinto_id))
    except Exception as e:
        flash(f"Error inesperado al guardar nueva versión: {str(e)}", "error")
        return redirect(url_for("versions.crear_version_form_route", recinto_id=recinto_id))


@versions_bp.route('/detalle/<int:version_id>')
def detalle_version_route(version_id): # Ruta de app.py para detalle_version_recinto
    detalles_version = obtener_detalles_version_recinto(version_id)
    if not detalles_version: # Si es un diccionario vacío o None
        flash("Versión de recinto no encontrada.", "error")
        # Redirigir a una página relevante, ej. el detalle del recinto padre si se tiene el ID
        # o a la lista de recintos.
        return redirect(url_for('theater.index'))


    zonas, pagination_obj = get_paginated_data(
        10, obtener_zonas_listado, obtener_total_zonas, version_id
    )
    data_zonas = {"zonas": zonas, "pagination": pagination_obj}
    return render_template(
        "config_theater_versions.html",
        detalles_version_recinto=detalles_version,
        data_zonas=data_zonas
    )

@versions_bp.route('/editar/<int:version_id>', methods=['POST']) # Solo POST para la acción
def editar_version_route(version_id): # Ruta de app.py para editar_version_recinto
    detalles_version_orig = obtener_detalles_version_recinto(version_id)
    if not detalles_version_orig:
        flash("Versión de recinto no encontrada", "error")
        return redirect(url_for("theater.index")) # O una página de error general

    # El método es POST
    nuevo_nombre = request.form["edit_name_version"]
    nuevo_svg = ""
    if 'edit_svg_version' in request.files and request.files['edit_svg_version'].filename != '':
        nuevo_svg = request.files["edit_svg_version"].read().decode("utf-8")

    nombre_original = detalles_version_orig.get("nombre_version_recinto")
    svg_original = detalles_version_orig.get("svg_version_recinto")

    cambios_realizados = False
    try:
        if nuevo_nombre != nombre_original and nuevo_svg and nuevo_svg != svg_original:
            actualizar_version_recinto(version_id, nuevo_nombre, nuevo_svg)
            flash("Nombre y SVG actualizados correctamente", "success")
            cambios_realizados = True
        elif nuevo_nombre != nombre_original:
            actualizar_version_recinto(version_id, nuevo_nombre, svg_original) # Pasa el svg original
            flash("Nombre actualizado correctamente", "success")
            cambios_realizados = True
        elif nuevo_svg and nuevo_svg != svg_original:
            actualizar_version_recinto(version_id, nombre_original, nuevo_svg) # Pasa el nombre original
            flash("SVG actualizado correctamente", "success")
            cambios_realizados = True

        if not cambios_realizados:
            flash("No se realizaron cambios", "warning")

    except Exception as e:
        flash(f"Error al actualizar la versión del recinto: {str(e)}", "error")

    return redirect(url_for("versions.detalle_version_route", version_id=version_id))