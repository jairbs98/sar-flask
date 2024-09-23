from flask import render_template, request
from flask_paginate import Pagination
from . import theater_blueprint
from app.routes import obtener_recintos_listado, obtener_total_recintos


@theater_blueprint.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    recintos = obtener_recintos_listado(page=page, per_page=per_page)
    total_recintos = obtener_total_recintos()
    pagination = Pagination(page=page, per_page=per_page, total=total_recintos, css_framework='bootstrap5')

    pag = {
        'recintos': recintos,
        'pagination': pagination
    }

    return render_template('theater/home.html', pag=pag)
