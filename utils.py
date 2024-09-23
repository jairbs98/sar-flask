from flask import request
from flask_paginate import Pagination


def inject_global_variables():
    return {
        # Nombres de campos
        'label_name': 'Nombre:',
        'label_address': 'Dirección:',
        'label_map': 'Mapa:',
        'label_svg': 'SVG:',
        'label_color': 'Color:',
        'label_status': 'Estatus:',
        'label_svg_id': 'ID SVG:',
        'label_capacity': 'Aforo:',
        # Nombres de botones
        'button_save': 'Guardar',
        'button_edit': 'Editar',
        'button_return': 'Regresar',
        'button_download': 'Descargar',
        'button_create_version': 'Crear versión',
        'button_create_area': 'Crear zona',
        'button_create_section': 'Crear sección',
        # Títulos
        'title_system': 'Sistema Administrador de Recintos',
        'title_create_theater': 'Crear recinto',
        'title_create_version': 'Crear versión de ',
        'title_create_area': 'Crear zona de ',
        'title_create_section': 'Crear sección de la zona ',
        'title_detail': 'Detalle de ',
        # Encabezados
        'header_id': 'ID',
        'header_name': 'Nombre',
        'header_address': 'Dirección',
        'header_color': 'Color',
        'header_id_svg': 'ID SVG',
        'header_capacity': 'Aforo',
        'header_status': 'Estatus',
        'header_creation_date': 'Fecha de creación',
        'header_modification_date': 'Fecha de modificación',
        'header_config': 'Ajustes',
        # ...
        'placeholder_name': 'Ingrese el nombre',
        'placeholder_address': 'Ingrese la dirección',
        'placeholder_map': 'Ingrese el mapa',
        'placeholder_id_svg': 'Ingrese el ID del SVG',
        'placeholder_capacity': 'Ingrese el aforo',
    }


def get_paginated_data(per_page, data_function, total_function, *args, **kwargs):
    page = request.args.get('page', 1, type=int)
    data = data_function(*args, page=page, per_page=per_page, **kwargs)
    total_data = total_function(*args, **kwargs)

    pagination = Pagination(page=page, per_page=per_page, total=total_data, css_framework='bootstrap5')

    return data, pagination
