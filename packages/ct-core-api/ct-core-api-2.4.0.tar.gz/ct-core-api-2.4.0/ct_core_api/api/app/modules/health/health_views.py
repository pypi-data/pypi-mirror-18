from flask import Blueprint

bp = Blueprint('health', __name__)


@bp.route('/ping')
def ping():
    """Simplistic health check route that many of our internal checks expect to exist."""
    return u'OK', 200
