import logging

from sqlalchemy import exc as sqa_exc, inspect, orm

from ct_core_api.api.common import selectors

_logger = logging.getLogger(__name__)


class ModelFieldSelectors(selectors.FieldSelectors):
    """A nested representation of a `Model` class's fields (named attributes)
    along with its sub-fields (nested relationships).
    """
    def __init__(self, model_cls, *model_fields, **model_sub_fields):
        super(ModelFieldSelectors, self).__init__(*model_fields, **model_sub_fields)
        self.model_cls = model_cls

    def __repr__(self):
        return "{}({}, {!r}, {!r})".format(
            self.__class__.__name__, self.model_cls.__name__, list(self.fields), self.sub_fields)

    @classmethod
    def from_field_selectors(cls, model_cls, field_selectors):
        """Create `ModelFieldSelectors` from the provided `Model` class and `FieldSelectors` instance."""
        def resolve_selectors(m_cls, fs):
            model_fields = []
            model_sub_fields = {}
            for f in fs.all_field_names:
                # If the model class has an attribute with this field name...
                if hasattr(m_cls, f):
                    try:
                        # and it represents a SQLAlchemy attribute like a column or relationship...
                        ia = inspect(getattr(m_cls, f))
                        if f in fs.sub_field_names:
                            # continue resolving the model fields for any relationships
                            model_sub_fields[f] = resolve_selectors(ia.mapper.class_, fs.sub_fields[f])
                        else:
                            # then add the field name to the list of model fields
                            model_fields.append(f)
                    except sqa_exc.NoInspectionAvailable:
                        pass

            return cls(m_cls, *model_fields, **model_sub_fields)

        # Resolve the model field selectors from the top-level model class
        return resolve_selectors(model_cls, field_selectors)

    def generate_loader_options(self, _context=None):
        """Generate a list of SQLAlchemy loader options based on the model fields described in this class.
        These are used to modify the state of a Query in order to affect how various mapped attributes are loaded.
        """
        if _context is None:
            r = [orm.load_only(*self.fields)]
            for k, v in self.sub_fields.iteritems():
                model_attr = getattr(self.model_cls, k)
                jl = orm.joinedload(model_attr, innerjoin=True)
                if not (hasattr(model_attr, 'nullable') and model_attr.nullable):
                    jl = orm.joinedload(model_attr, innerjoin=False)
                r.append(v.generate_loader_options(_context=jl))
            return r
        else:
            r = _context.load_only(*self.fields)
            if len(self.sub_fields) > 1:
                raise Exception(
                    'Unable to generate loader options. Too many sub-fields exist below the top-most level.')
            else:
                for k, v in self.sub_fields.iteritems():
                    model_attr = getattr(self.model_cls, k)
                    # Assume that a relationship specifying an "order by" clause is not suitable for an inner join
                    if model_attr.property.order_by:
                        r = r.subqueryload(model_attr)
                    else:
                        if hasattr(model_attr, 'nullable') and model_attr.nullable:
                            r = r.joinedload(model_attr)
                        else:
                            r = r.joinedload(model_attr, innerjoin=True)
                    return v.generate_loader_options(_context=r)
            return r
