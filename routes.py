from flask import request, render_template, redirect, url_for, flash
from utils import get_paginated_data
from db_queries import *


def versiones_recinto(recinto_id):
    detalles_recinto = obtener_detalles_recinto(recinto_id)
    version_recinto = obtener_versiones_recinto(recinto_id)
    return render_template('theater_versions/form_create_theater_version.html', detalles_recinto=detalles_recinto,
                           version_recinto=version_recinto)


def crear_zona(id_version):
    detalles_recinto = obtener_detalles_version_recinto(id_version)
    return render_template('theater_areas/form_create_theater_area.html', detalles_recinto=detalles_recinto)


def detalle_zonas(id_zona):
    detalles_zona = obtener_detalles_zona(id_zona)
    svg_recinto_por_zona = obtener_svg_recinto_por_zona(id_zona)
    secciones, pagination = get_paginated_data(10, obtener_secciones_listado, obtener_total_secciones, id_zona)

    data = {
        'secciones': secciones,
        'pagination': pagination
    }
    return render_template('theater_areas/config_theater_areas.html', detalles_zona=detalles_zona,
                           svg_recinto_por_zona=svg_recinto_por_zona, data=data)


def detalle_seccion(id_seccion):
    detalles_seccion = obtener_detalles_config_seccion(id_seccion)
    return render_template('theater_sections/config_theater_sections.html', detalles_seccion=detalles_seccion)


def crear_seccion(id_zona):
    detalles_seccion = obtener_detalles_seccion(id_zona)
    return render_template('theater_sections/form_create_theater_sections.html', detalles_seccion=detalles_seccion)


def detalle_recinto(recinto_id):
    detalles_recinto = obtener_detalles_recinto(recinto_id)
    versiones, pagination = get_paginated_data(10, obtener_versiones_listado, obtener_total_versiones, recinto_id)
    pag_v = {
        'versiones': versiones,
        'pagination': pagination
    }
    return render_template('theater/config_theater.html', detalles_recinto=detalles_recinto, pag_v=pag_v)


def detalle_version_recinto(version_id):
    detalles_version_recinto = obtener_detalles_version_recinto(version_id)
    zonas, pagination = get_paginated_data(10, obtener_zonas_listado, obtener_total_zonas, version_id)

    data_zonas = {
        'zonas': zonas,
        'pagination': pagination
    }
    return render_template('theater_versions/config_theater_versions.html',
                           detalles_version_recinto=detalles_version_recinto, data_zonas=data_zonas)


def guardar_recinto_principal():
    try:
        name = request.form['name']
        address = request.form['address']
        map = request.form['map']
        flash('Recinto guardado exitosamente', 'success')
        guardar_recinto(name, address, map)

        return redirect(url_for('index'))
    except KeyError as e:
        flash(f'Error al guardar: {str(e)}', 'error')
    except Exception as e:
        flash(f'Error inesperado al guardar: {str(e)}', 'error')

    return redirect(url_for('index'))


def guardar_version_recinto(recinto_id):
    try:
        nom_version = request.form['nom_version']
        svg_recinto = request.files['svg_recinto'].read().decode('utf-8')

        flash('Nueva versión guardada exitosamente', 'success')

        guardar_nueva_version_recinto(recinto_id, nom_version, svg_recinto)

        return redirect(url_for('detalle_recinto', recinto_id=recinto_id))

    except KeyError as e:
        return f'Error al guardar nueva versión: {str(e)}'

    except Exception as e:
        return f'Error inesperado al guardar nueva versión: {str(e)}'


def guardar_zona(id_version):
    try:
        nombre_zona = request.form['nombre_zona']
        color_zona = request.form['area_color']

        flash('Nueva zona guardada exitosamente', 'success')

        guardar_nueva_zona(id_version, nombre_zona, color_zona)

        return redirect(url_for('crear_zona', id_version=id_version))

    except KeyError as e:
        return f'Error al guardar nueva zona: {str(e)}'

    except Exception as e:
        return f'Error inesperado al guardar nueva zona: {str(e)}'


def guardar_seccion(id_zona):
    try:
        nombre_seccion = request.form['nombre_seccion']
        id_svg = request.form['id_svg']
        aforo = request.form['aforo_seccion']

        flash('Nueva sección guardada exitosamente', 'success')

        guardar_nueva_seccion(id_zona, nombre_seccion, id_svg, aforo)

        return redirect(url_for('crear_seccion', id_zona=id_zona))

    except KeyError as e:
        return f'Error al guardar nueva seccion: {str(e)}'

    except Exception as e:
        return f'Error inesperado al guardar nueva sección: {str(e)}'


def editar_recinto(recinto_id):
    detalles_recinto = obtener_detalles_recinto(recinto_id)

    if detalles_recinto is None:
        flash('Recinto no encontrado', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        nuevo_nombre = request.form['edit_name']
        nueva_direccion = request.form['edit_address']
        nuevo_mapa = request.form['add_map']

        if nuevo_nombre != detalles_recinto['nombre'] or nueva_direccion != detalles_recinto[
            'direccion'] or nuevo_mapa != detalles_recinto['mapa']:
            actualizar_recinto(recinto_id, nuevo_nombre, nueva_direccion, nuevo_mapa)

            flash('Actualizado correctamente', 'success')
            return redirect(url_for('detalle_recinto', recinto_id=recinto_id))

        flash('No se realizaron cambios', 'warning')

    return redirect(url_for('detalle_recinto', recinto_id=recinto_id))


def editar_version_recinto(version_id):
    detalles_version_recinto = obtener_detalles_version_recinto(version_id)
    if detalles_version_recinto is None:
        flash('Versión de recinto no encontrada', 'error')
        return redirect(url_for('detalle_version_recinto'))

    if request.method == 'POST':
        nuevo_nombre = request.form['edit_name_version']
        nuevo_svg = request.files['edit_svg_version'].read().decode('utf-8')

        nombre_original = detalles_version_recinto['nombre_version_recinto']
        svg_original = detalles_version_recinto['svg_version_recinto']

        try:
            if nuevo_nombre != nombre_original and nuevo_nombre and nuevo_svg != svg_original and nuevo_svg:
                flash('Nombre y SVG actualizados correctamente', 'success')
                actualizar_version_recinto(version_id, nuevo_nombre, nuevo_svg)
            elif nuevo_nombre != nombre_original and nuevo_nombre:
                actualizar_version_recinto(version_id, nuevo_nombre, svg_original)
                flash('Nombre actualizado correctamente', 'success')
            elif nuevo_svg != svg_original and nuevo_svg:
                actualizar_version_recinto(version_id, nombre_original, nuevo_svg)
                flash('SVG actualizado correctamente', 'success')
            else:
                flash('No se realizaron cambios', 'warning')

        except Exception as e:
            flash(f'Error al actualizar la versión del recinto: {str(e)}', 'error')

        return redirect(url_for('detalle_version_recinto', version_id=version_id))

    return redirect(url_for('detalle_version_recinto', version_id=version_id))


def editar_zona(id_zona):
    detalles_zona = obtener_detalles_zona(id_zona)

    if detalles_zona is None:
        flash('Zona no encontrada', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        nuevo_nombre = request.form['edit_area_name']
        nuevo_color = request.form['edit_area_color']
        nuevo_estatus = request.form.get('edit_status', False)

        if nuevo_nombre != detalles_zona['nombre_zona'] or nuevo_color != detalles_zona[
            'color_zona'] or nuevo_estatus != detalles_zona['estatus_zona']:
            actualizar_zona(id_zona, nuevo_nombre, nuevo_color, nuevo_estatus)

            flash('Actualizado correctamente', 'success')
            return redirect(url_for('detalle_zonas', id_zona=id_zona))

        flash('No se realizaron cambios', 'warning')

    return redirect(url_for('detalle_zonas', id_zona=id_zona))


# Pendiente de adaptar
def editar_seccion(id_zona):
    detalles_zona = obtener_detalles_zona(id_zona)

    if detalles_zona is None:
        flash('Zona no encontrada', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        nuevo_nombre = request.form['edit_area_name']
        nuevo_color = request.form['edit_area_color']
        nuevo_estatus = request.form.get('edit_status', False)

        if nuevo_nombre != detalles_zona['nombre_zona'] or nuevo_color != detalles_zona[
            'color_zona'] or nuevo_estatus != detalles_zona['estatus_zona']:
            actualizar_zona(id_zona, nuevo_nombre, nuevo_color, nuevo_estatus)

            flash('Actualizado correctamente', 'success')
            return redirect(url_for('detalle_zonas', id_zona=id_zona))

        flash('No se realizaron cambios', 'warning')

    return redirect(url_for('detalle_zonas', id_zona=id_zona))


def editar_detalle_seccion(id_seccion):
    detalles_seccion = obtener_detalles_config_seccion(id_seccion)

    if detalles_seccion is None:
        flash('Sección no encontrada', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        new_svg_width = request.form['edit_svg_width']
        new_svg_height = request.form['edit_svg_height']
        new_axis = request.form.get('edit_axis', False)
        new_theater_name = request.form['edit_theater_name']
        new_alignment = request.form.get('edit_alignment', False)
        new_initial_position_x = request.form['edit_initial_position_x']
        new_initial_position_y = request.form['edit_initial_position_y']
        new_line_spacing = request.form['edit_line_spacing']
        new_position_increment_x = request.form['edit_position_increment_x']
        new_position_increment_y = request.form['edit_position_increment_y']
        new_seat_form = request.form['edit_seat_form']

        actualizar_detalles_seccion(id_seccion,
                                    new_svg_width, new_svg_height, new_axis, new_theater_name,
                                    new_alignment, new_initial_position_x, new_initial_position_y,
                                    new_line_spacing, new_position_increment_x, new_position_increment_y,
                                    new_seat_form)

        flash('Sección actualizada correctamente', 'success')

    return redirect(url_for('detalle_seccion', id_seccion=id_seccion))


def index():
    recintos, pagination = get_paginated_data(5, obtener_recintos_listado, obtener_total_recintos)

    pag = {
        'recintos': recintos,
        'pagination': pagination
    }

    return render_template('theater/home.html', pag=pag)
