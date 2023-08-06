import pytest

from ct_core_api.api.app.extensions import debug_api_ext
from tests import utils


@pytest.mark.parametrize('api_version', ['2.0'])
def test_debug_api_extension_availability(api_version):
    api_ext_version = api_version.replace('.', '_')
    assert hasattr(debug_api_ext, "debug_api_v{}".format(api_ext_version))


@pytest.mark.parametrize('api_version', ['2.0'])
def test_debug_api_spec_validity(app_client, api_version):
    utils.validate_openapi_spec(app_client, "debug-api-v{}.specs".format(api_version))
