from flask import Blueprint, render_template, request, redirect, url_for, flash
# from ..utils import get_paginated_data # Si se necesita paginación aquí
from db_queries import (
    obtener_detalles_seccion, # Para el contexto al crear una sección
    obtener_detalles_config_seccion, # Para el detalle/config de una sección
    guardar_nueva_seccion,       # Anteriormente guardar_seccion
    actualizar_detalles_seccion # Anteriormente editar_detalle_seccion
    # editar_seccion no está completamente implementada en el original, así que se omite por ahora
)

sections_bp = Blueprint(
    'sections',
    __name__,
    template_folder='../templates/theater_sections',
    url_prefix='/secciones'
)

# Ruta para mostrar el formulario de creación de sección
@sections_bp.route('/crear/para-zona/<int:id_zona>')
def crear_seccion_form_route(id_zona): # Ruta de app.py para crear_seccion
    # obtener_detalles_seccion(id_zona) en el original parece obtener detalles de la ZONA, no de una SECCIÓN.
    # Renombrar la función en db_queries o clarificar su propósito sería bueno.
    # Asumiendo que obtiene detalles de la ZONA para dar contexto:
    detalles_zona_contexto = obtener_detalles_seccion(id_zona) # Esta función obtiene datos de la ZONA
    if not detalles_zona_contexto:
        flash("Zona no encontrada para crear sección.", "error")
        return redirect(url_for('theater.index')) # O a la lista de zonas/versiones
    return render_template(
        "form_create_theater_sections.html",
        detalles_seccion=detalles_zona_contexto # La plantilla espera 'detalles_seccion' pero es contexto de ZONA
    )
    
@sections_bp.route('/editar-basico/<int:id_seccion>', methods=['POST'])
def editar_seccion_basica_route(id_seccion):
    # Obtener los datos del formulario (los que están en el primer <form id="edit_form">)
    if request.method == 'POST':
        try:
            nuevo_nombre = request.form.get('edit_section_name')
            nuevo_id_svg = request.form.get('edit_id_svg')
            nuevo_aforo_str = request.form.get('edit_capacity')
            # El campo hidden 'edit_status_hidden_basic' envía 'true' o 'false' como string
            nuevo_estatus_str = request.form.get('edit_status_hidden_basic', 'false') 
            
            nuevo_aforo = int(nuevo_aforo_str) if nuevo_aforo_str else None # Convertir a int si no es None
            nuevo_estatus_bool = nuevo_estatus_str.lower() == 'true'

            # Llama a una función en db_queries.py para actualizar estos datos básicos
            # Deberás crear esta función 'actualizar_seccion_basica' en db_queries.py
            actualizar_seccion_basica(
                id_seccion,
                nuevo_nombre,
                nuevo_id_svg,
                nuevo_aforo,
                nuevo_estatus_bool
            )
            flash('Información básica de la sección actualizada correctamente.', 'success')
        except ValueError:
            flash('Error: El aforo debe ser un número.', 'danger')
        except Exception as e:
            flash(f'Error al actualizar la información básica de la sección: {str(e)}', 'danger')
            # current_app.logger.error(f"Error en editar_seccion_basica_route: {e}") # Si tienes logging configurado
            print(f"Error en editar_seccion_basica_route: {e}")


    # Redirige de vuelta a la página de detalle de la sección
    return redirect(url_for('sections.detalle_seccion_route', id_seccion=id_seccion))

@sections_bp.route('/guardar/para-zona/<int:id_zona>', methods=['POST'])
def guardar_seccion_route(id_zona): # Ruta de app.py para guardar_seccion
    try:
        nombre_seccion = request.form["nombre_seccion"]
        id_svg = request.form["id_svg"]
        aforo = request.form["aforo_seccion"]
        flash("Nueva sección guardada exitosamente", "success")
        guardar_nueva_seccion(id_zona, nombre_seccion, id_svg, aforo)
        return redirect(url_for('sections.crear_seccion_form_route', id_zona=id_zona))
    except KeyError as e:
        flash(f"Error al guardar nueva sección: Falta el campo {str(e)}", "error")
        return redirect(url_for('sections.crear_seccion_form_route', id_zona=id_zona))
    except Exception as e:
        flash(f"Error inesperado al guardar nueva sección: {str(e)}", "error")
        return redirect(url_for('sections.crear_seccion_form_route', id_zona=id_zona))

@sections_bp.route('/detalle/<int:id_seccion>')
def detalle_seccion_route(id_seccion): # Ruta de app.py para detalle_seccion
    detalles_seccion_data = obtener_detalles_config_seccion(id_seccion)
    if not detalles_seccion_data:
        flash("Sección no encontrada.", "error")
        return redirect(url_for('theater.index')) # O a la lista de zonas
    return render_template(
        "config_theater_sections.html",
        detalles_seccion=detalles_seccion_data
    )

@sections_bp.route('/editar-detalles/<int:id_seccion>', methods=['POST'])
def editar_detalle_seccion_route(id_seccion): # Ruta de app.py para editar_detalle_seccion
    detalles_seccion_orig = obtener_detalles_config_seccion(id_seccion)
    if not detalles_seccion_orig:
        flash("Sección no encontrada", "error")
        # Redirigir a una página apropiada, ej. detalle de la zona
        return redirect(url_for("theater.index")) # Placeholder

    # El método es POST
    new_svg_width = request.form.get("edit_svg_width")
    new_svg_height = request.form.get("edit_svg_height")
    new_axis = request.form.get("edit_axis_hidden") == 'true' if request.form.get("edit_axis_hidden") else False
    new_theater_name = request.form.get("edit_theater_name")
    new_alignment = request.form.get("edit_alignment_hidden") == 'true' if request.form.get("edit_alignment_hidden") else False
    new_initial_position_x = request.form.get("edit_initial_position_x")
    new_initial_position_y = request.form.get("edit_initial_position_y")
    new_line_spacing = request.form.get("edit_line_spacing")
    new_position_increment_x = request.form.get("edit_position_increment_x")
    new_position_increment_y = request.form.get("edit_position_increment_y")
    new_seat_form = request.form.get("edit_seat_form")

    # Aquí deberías comparar si hubo cambios antes de llamar a actualizar y flashear.
    # Por simplicidad, se llama directamente.
    try:
        actualizar_detalles_seccion(
            id_seccion, new_svg_width, new_svg_height, new_axis,
            new_theater_name, new_alignment, new_initial_position_x,
            new_initial_position_y, new_line_spacing, new_position_increment_x,
            new_position_increment_y, new_seat_form
        )
        flash("Detalles de sección actualizados correctamente", "success")
    except Exception as e:
        flash(f"Error al actualizar detalles de la sección: {str(e)}", "error")

    return redirect(url_for("sections.detalle_seccion_route", id_seccion=id_seccion))