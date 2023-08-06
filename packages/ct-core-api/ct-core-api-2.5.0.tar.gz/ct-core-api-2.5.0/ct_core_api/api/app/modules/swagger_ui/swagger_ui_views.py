import logging

from flask import Blueprint, url_for

_logger = logging.getLogger(__name__)


bp = Blueprint(
    'swagger-ui',
    __name__,
    template_folder='templates',
    static_folder='../../static',
    static_url_path='/swagger')


@bp.add_app_template_global
def swagger_ui_static(filename):
    return url_for('swagger-ui.static', filename="swagger-ui/{0}".format(filename))
