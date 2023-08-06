from flask import Blueprint, current_app, url_for

from ct_core_api.common import app_utils

INDEX_ENDPOINT_SUFFIXES = ['.index', '.doc', '.specs']

bp = Blueprint('index', __name__)


@bp.route('/')
@app_utils.template(template='index/index.html')
def root():
    return dict(urls=sorted(
        [url_for(x) for x in current_app.view_functions.keys() if any(x.endswith(y) for y in INDEX_ENDPOINT_SUFFIXES)]))
