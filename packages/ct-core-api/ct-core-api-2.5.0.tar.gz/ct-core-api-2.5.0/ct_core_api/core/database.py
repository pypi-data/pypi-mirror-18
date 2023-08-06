from ct_core_db import db  # noqa
from ct_core_db.lib import sqla


def _init():
    # Configure the conversion functions for internal/external ids
    from ct_core_api.api.common import api_helpers as ah
    sqla.HasExternalId._to_internal_func = ah.from_external_id
    sqla.HasExternalId._to_external_func = ah.to_external_id

_init()
