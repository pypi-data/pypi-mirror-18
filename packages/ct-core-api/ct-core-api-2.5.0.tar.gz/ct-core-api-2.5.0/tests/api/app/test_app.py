import pytest

from ct_core_api.api.app.factory import create_api_app, CONFIG_NAME_MAPPER


@pytest.mark.parametrize('flask_config', ['production', 'development', 'testing'])
def test_create_app_success(flask_config):
    app = create_api_app(__name__, flask_config_name=flask_config)

    if flask_config == 'development':
        assert app.debug
        assert not app.testing
    elif flask_config == 'testing':
        assert not app.debug
        assert app.testing
    elif flask_config == 'production':
        assert not app.debug
        assert not app.testing


def test_create_app_failure_with_non_existing_config():
    with pytest.raises(KeyError):
        create_api_app(__name__, flask_config_name='non-existing-config')


def test_create_app_failure_with_broken_import_config():
    CONFIG_NAME_MAPPER['broken-import-config'] = 'broken-import-config'
    with pytest.raises(ImportError):
        create_api_app(__name__, flask_config_name='broken-import-config')
    del CONFIG_NAME_MAPPER['broken-import-config']
