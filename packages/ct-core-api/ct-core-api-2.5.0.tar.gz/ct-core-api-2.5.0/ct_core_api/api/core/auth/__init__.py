from collections import namedtuple
from functools import wraps

from flask import g
from flask_principal import AnonymousIdentity, Permission


########################################
# Needs
########################################

ResourceNeed = namedtuple('ResourceNeed', ['resource', 'id'])
ResourceTypeNeed = namedtuple('ResourceTypeNeed', ['resource', 'type'])

ResourceActionNeed = namedtuple('ResourceActionNeed', ['resource', 'action', 'id'])
ResourceAssociationNeed = namedtuple('ResourceAssociationNeed', ['resource', 'association', 'id'])
ResourceUserTypeNeed = namedtuple('ResourceUserTypeNeed', ['resource', 'user_type', 'id'])

ResourceUserTypeAssociationNeed = namedtuple('ResourceUserTypeAssociationNeed', ['resource', 'user_type', 'association', 'id'])
ResourceUserRoleAssociationNeed = namedtuple('ResourceUserRoleAssociationNeed', ['resource', 'user_role', 'association', 'id'])


########################################
# Identity
########################################

def update_identity_with_needs(needs):
    """Update the current identity with the provided set of `needs`,
    unless the current identity is anonymous (ie. unauthenticated).
    """
    if not isinstance(g.identity, AnonymousIdentity):
        g.identity.provides.update(needs)


def update_identity_fn_factory(needs_fn):
    """Create a decorator function that updates the current identity with the needs returned from the `needs_fn`.
    The `needs_fn` takes the current user (from the identity) as it's only argument.
    """
    def _update_identity_fn(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            update_identity_with_needs(needs_fn(g.identity.user))
            return f(*args, **kwargs)
        return decorated
    return _update_identity_fn


########################################
# Permissions
########################################

class CompositeOrPermission(Permission):
    """Compose two or more permissions into one.
    The `Need`s for this permission will be the union of those from every underlying permission.
    Therefore, if at least one underlying permission allows access, then this permission allows access.
    """

    def __init__(self, *permissions):
        if not len(permissions) > 1:
            raise ValueError('At least two permissions are required')

        for perm in permissions:
            if not isinstance(perm, Permission):
                raise TypeError("Invalid Permission: {}".format(perm))

        self.permissions = permissions

        super(CompositeOrPermission, self).__init__(*set.union(*[x.needs for x in self.permissions]))

    def __str__(self):
        """String representation of the underlying permissions."""
        return ', '.join([str(perm) for perm in self.permissions])

    class Doc(object):
        """Use this to document CompositeOrPermissions. """

        def __init__(self, *permission_classes):
            self.permission_classes = permission_classes

        def __str__(self):
            return '(' + ' OR '.join([cls.__name__ for cls in self.permission_classes]) + ')'
