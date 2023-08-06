from flask import url_for

from ct_core_api.common import app_utils


INDEX_ENDPOINT_SUFFIXES = ['.index', '.doc', '.specs']


def init_app(app):
    @app.route('/')
    @app_utils.template(template='_index.html')
    def index():
        return dict(urls=sorted(
            [url_for(x) for x in app.view_functions.keys() if any(x.endswith(y) for y in INDEX_ENDPOINT_SUFFIXES)]))
