import pytest

from ct_core_api.api.app.extensions import debug_api_ext


@pytest.mark.parametrize('api_version', ['1'])
def test_debug_api_extension_availability(api_version):
    assert hasattr(debug_api_ext, "debug_api_v{}".format(api_version))
