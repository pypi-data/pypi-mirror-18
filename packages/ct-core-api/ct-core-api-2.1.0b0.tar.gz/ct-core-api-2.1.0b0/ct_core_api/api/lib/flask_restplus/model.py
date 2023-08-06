from apispec.ext.marshmallow.swagger import fields2jsonschema

from flask_restplus.model import Model as OriginalModel
from werkzeug.utils import cached_property


class Model(OriginalModel):
    def __init__(self, name, model, **kwargs):
        # XXX: Wrapping with __schema__ is not a very elegant solution.
        super(Model, self).__init__(name, {'__schema__': model}, **kwargs)

    @cached_property
    def __schema__(self):
        return fields2jsonschema(self['__schema__'].fields)
