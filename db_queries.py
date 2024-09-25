from db.db_service import DataBaseFunctions
from db.db_config import DB_CONFIG


def ejecutar_query(query, values=None, fetch_results=True, commit=False):
    db_functions = DataBaseFunctions(**DB_CONFIG)
    try:
        return db_functions.execute_query(query, values, fetch_results, commit)
    finally:
        db_functions.close()


def guardar_recinto(name, address, map):
    query = "SELECT * FROM proc_guardar_recinto (%s, %s, %s)"
    values = (name, address, map)
    ejecutar_query(query, values)


def obtener_total_recintos():
    query = "SELECT COUNT(*) FROM proc_obtener_recintos()"
    total_recintos = ejecutar_query(query, fetch_results=True)
    return total_recintos[0][0] if total_recintos else 0


def obtener_recintos_listado(page=1, per_page=5):
    offset = (page - 1) * per_page
    query = f"SELECT * FROM proc_obtener_recintos() OFFSET {offset} LIMIT {per_page}"
    resultados = ejecutar_query(query)
    return resultados


def obtener_detalles_recinto(recinto_id):
    query = "SELECT * FROM recintos WHERE id_recinto = %s"
    values = (recinto_id,)
    detalles_recinto = ejecutar_query(query, values, fetch_results=True)
    if detalles_recinto and len(detalles_recinto) >= 1:
        detalle_recinto_tupla = detalles_recinto[0]
        return {
            "id": detalle_recinto_tupla[0],
            "nombre": detalle_recinto_tupla[1],
            "direccion": detalle_recinto_tupla[2],
            "mapa": detalle_recinto_tupla[5],
        }
    else:
        return None


def obtener_detalles_version_recinto(id_version):
    query = "SELECT * FROM cat_recintos WHERE id_vrecinto = %s ORDER BY id_vrecinto;"
    values = (id_version,)
    detalles_version_recinto = ejecutar_query(query, values, fetch_results=True)
    if detalles_version_recinto and len(detalles_version_recinto) >= 1:
        detalle_version_recinto_tupla = detalles_version_recinto[0]
        return {
            "id_version_recinto": detalle_version_recinto_tupla[0],
            "id_recinto": detalle_version_recinto_tupla[1],
            "nombre_version_recinto": detalle_version_recinto_tupla[2],
            "svg_version_recinto": detalle_version_recinto_tupla[3],
            "opc_activo_version_recinto": detalle_version_recinto_tupla[5],
        }
    else:
        return {}


def obtener_secciones(id_zona):
    query = "SELECT * FROM secciones WHERE id_zonas = %s ORDER BY id_seccion;"
    values = (id_zona,)
    detalles_secciones = ejecutar_query(query, values, fetch_results=True)
    if detalles_secciones and len(detalles_secciones) >= 1:
        secciones_tupla = detalles_secciones[0]
        return {
            "id_seccion": secciones_tupla[0],
            "id_zona": secciones_tupla[1],
            "nombre_seccion": secciones_tupla[2],
            "id_svg": secciones_tupla[3],
            "aforo": secciones_tupla[4],
            "fecha_registro": secciones_tupla[5],
            "fecha_modificacion": secciones_tupla[6],
        }
    else:
        return {}


def obtener_detalles_zona(id_zona):
    query = "SELECT * FROM zonas WHERE id_zona = (%s);"
    values = (id_zona,)
    detalles_zonas = ejecutar_query(query, values, fetch_results=True)
    if detalles_zonas and len(detalles_zonas) >= 1:
        detalle_zonas_tupla = detalles_zonas[0]
        return {
            "id_zona": detalle_zonas_tupla[0],
            "id_version_recinto": detalle_zonas_tupla[1],
            "nombre_zona": detalle_zonas_tupla[2],
            "color_zona": detalle_zonas_tupla[3],
            "fecha_registro_zona": detalle_zonas_tupla[4],
            "estatus_zona": detalle_zonas_tupla[5],
        }
    else:
        return {}


def obtener_detalles_seccion(id_seccion):
    query = "SELECT * FROM zonas WHERE id_zona = (%s);"
    values = (id_seccion,)
    detalles_zonas = ejecutar_query(query, values, fetch_results=True)
    if detalles_zonas and len(detalles_zonas) >= 1:
        detalle_zonas_tupla = detalles_zonas[0]
        return {
            "id_zona": detalle_zonas_tupla[0],
            "id_version_recinto": detalle_zonas_tupla[1],
            "nombre_zona": detalle_zonas_tupla[2],
            "color_zona": detalle_zonas_tupla[3],
            "fecha_registro_zona": detalle_zonas_tupla[4],
            "estatus_zona": detalle_zonas_tupla[5],
        }
    else:
        return {}


def obtener_detalles_config_seccion(id_seccion):
    query = "SELECT * FROM proc_obtener_seccion_con_detalle (%s);"
    values = (id_seccion,)
    detalles_seccion = ejecutar_query(query, values, fetch_results=True)
    if detalles_seccion and len(detalles_seccion) >= 1:
        detalle_seccion_tupla = detalles_seccion[0]
        return {
            "id_seccion": detalle_seccion_tupla[0],
            "id_zona": detalle_seccion_tupla[1],
            "nom_seccion": detalle_seccion_tupla[2],
            "id_svg": detalle_seccion_tupla[3],
            "aforo_seccion": detalle_seccion_tupla[4],
            "fec_registro_seccion": detalle_seccion_tupla[5],
            "fec_modificacion_seccion": detalle_seccion_tupla[6],
            "opc_activo_seccion": detalle_seccion_tupla[7],
            "id_detalle_seccion": detalle_seccion_tupla[8],
            "ancho_svg": detalle_seccion_tupla[9],
            "alto_svg": detalle_seccion_tupla[10],
            "num_filas": detalle_seccion_tupla[11],
            "num_columnas": detalle_seccion_tupla[12],
            "orientacion_distribucion": detalle_seccion_tupla[13],
            "orientacion_escenario": detalle_seccion_tupla[14],
            "nombre_escenario": detalle_seccion_tupla[15],
            "posicion_inicial_x": detalle_seccion_tupla[16],
            "posicion_inicial_y": detalle_seccion_tupla[17],
            "incremento_interlineado": detalle_seccion_tupla[18],
            "forma_asiento": detalle_seccion_tupla[19],
            "incremento_x": detalle_seccion_tupla[20],
            "incremento_y": detalle_seccion_tupla[21],
            "direccion_numerado": detalle_seccion_tupla[22],
            "arreglo_info": detalle_seccion_tupla[23],
            "arreglo_posicion": detalle_seccion_tupla[24],
            "svg_seccion": detalle_seccion_tupla[25],
        }
    else:
        return {}


def obtener_svg_recinto_por_zona(id_zona):
    query = "SELECT * FROM proc_obtener_svg_recinto (%s)"
    values = (id_zona,)
    svg_por_zona = ejecutar_query(query, values, fetch_results=True)
    if svg_por_zona and len(svg_por_zona) >= 1:
        svg_por_zona_tupla = svg_por_zona[0]
        return {"svg_recinto": svg_por_zona_tupla[0]}
    else:
        return {}


def actualizar_recinto(recinto_id, nuevo_nombre, nueva_direccion, nuevo_mapa):
    query = "SELECT * FROM proc_actualizar_recinto (%s, %s, %s, %s)"
    values = (nuevo_nombre, nueva_direccion, nuevo_mapa, recinto_id)
    ejecutar_query(query, values, fetch_results=False)


def actualizar_version_recinto(id_version, nuevo_nombre, nuevo_svg):
    query = "SELECT * FROM proc_actualizar_version_recinto (%s, %s, %s)"
    values = (nuevo_nombre, nuevo_svg, id_version)
    ejecutar_query(query, values, fetch_results=False)


def actualizar_zona(id_zona, nuevo_nombre, nuevo_color, nuevo_opc_activo):
    query = "UPDATE zonas SET nom_zona = %s, color_zona = %s, opc_activo = %s WHERE id_zona = %s"
    values = (nuevo_nombre, nuevo_color, nuevo_opc_activo, id_zona)
    ejecutar_query(query, values, fetch_results=False)


def actualizar_detalles_seccion(
    id_seccion,
    new_svg_width,
    new_svg_height,
    new_axis,
    new_theater_name,
    new_alignment,
    new_initial_position_x,
    new_initial_position_y,
    new_line_spacing,
    new_position_increment_x,
    new_position_increment_y,
    new_seat_form,
):
    query = "SELECT * FROM proc_actualizar_ctl_seccion(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (
        new_svg_width,
        new_svg_height,
        new_axis,
        new_alignment,
        new_theater_name,
        new_initial_position_x,
        new_initial_position_y,
        new_line_spacing,
        new_seat_form,
        new_position_increment_x,
        new_position_increment_y,
        id_seccion,
    )
    ejecutar_query(query, values, fetch_results=False)


def guardar_nueva_version_recinto(recinto_id, nom_version, svg_recinto):
    query = "INSERT INTO cat_recintos (id_recinto, nom_version, svg_recinto) VALUES (%s, %s, %s)"
    values = (recinto_id, nom_version, svg_recinto)
    ejecutar_query(query, values, fetch_results=False)


def guardar_nueva_zona(recinto_id, nombre_zona, color_zona):
    query = "INSERT INTO zonas (id_vrecinto, nom_zona, color_zona) VALUES (%s, %s, %s)"
    values = (recinto_id, nombre_zona, color_zona)
    ejecutar_query(query, values, fetch_results=False)


def guardar_nueva_seccion(recinto_id, nombre_seccion, id_svg, aforo_seccion):
    query = "SELECT * FROM proc_guardar_seccion (%s, %s, %s, %s)"
    values = (recinto_id, nombre_seccion, id_svg, aforo_seccion)
    ejecutar_query(query, values, fetch_results=False)


def obtener_versiones_recinto(recinto_id):
    query = "SELECT * FROM proc_consultar_cat_recinto (%s)"
    values = (recinto_id,)
    versiones_recintos = ejecutar_query(query, values, fetch_results=True)
    return versiones_recintos


def obtener_total_versiones(recinto_id):
    query = "SELECT COUNT(*) FROM proc_obtener_versiones(%s)"
    total_versiones = ejecutar_query(query, (recinto_id,), fetch_results=True)
    return total_versiones[0][0] if total_versiones else 0


def obtener_versiones_listado(recinto_id, page=1, per_page=5):
    offset = (page - 1) * per_page
    query = "SELECT * FROM proc_obtener_versiones(%s) OFFSET %s LIMIT %s"
    values = (recinto_id, offset, per_page)
    versiones = ejecutar_query(query, values, fetch_results=True)
    return versiones


def obtener_total_zonas(id_version):
    query = "SELECT COUNT(*) FROM proc_obtener_zonas(%s)"
    total_zonas = ejecutar_query(query, (id_version,), fetch_results=True)
    return total_zonas[0][0] if total_zonas else 0


def obtener_zonas_listado(id_version, page=1, per_page=5):
    offset = (page - 1) * per_page
    query = "SELECT * FROM proc_obtener_zonas(%s) OFFSET %s LIMIT %s"
    values = (id_version, offset, per_page)
    zonas = ejecutar_query(query, values, fetch_results=True)
    return zonas


def obtener_total_secciones(id_zona):
    query = "SELECT COUNT(*) FROM proc_obtener_secciones(%s)"
    total_zonas = ejecutar_query(query, (id_zona,), fetch_results=True)
    return total_zonas[0][0] if total_zonas else 0


def obtener_secciones_listado(id_zona, page=1, per_page=5):
    offset = (page - 1) * per_page
    query = "SELECT * FROM proc_obtener_secciones(%s) OFFSET %s LIMIT %s"
    values = (id_zona, offset, per_page)
    zonas = ejecutar_query(query, values, fetch_results=True)
    return zonas
