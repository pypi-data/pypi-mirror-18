import pytest

from tests import utils


def create_test_app():
    from ct_core_api.api.app.factory import create_api_app
    return create_api_app(__name__, flask_config_name='testing')


@pytest.yield_fixture(scope='session')
def app():
    from ct_core_api.core.database import db
    app = create_test_app()

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.yield_fixture()
def db(app):
    from ct_core_api.core.database import db as db_instance
    yield db_instance
    db_instance.session.rollback()


@pytest.fixture(scope='session')
def app_client(app):
    app.test_client_class = utils.AppClient
    app.response_class = utils.AppResponse
    return app.test_client()


@pytest.fixture(scope='session')
def core_api(app):
    from ct_core_api.api.core.api import API
    api = API()
    api.init_app(app)
    return api
