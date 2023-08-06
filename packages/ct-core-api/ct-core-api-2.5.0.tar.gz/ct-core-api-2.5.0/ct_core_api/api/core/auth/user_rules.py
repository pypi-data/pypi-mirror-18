from flask_login import current_user

from ct_core_api.api.core import response
from ct_core_api.api.core.auth.rules import DenyAbortMixin, Rule


class WriteAccessRule(DenyAbortMixin, Rule):
    """
    Ensure that the current_user has has write access.
    """

    def check(self):
        return current_user.is_regular


class ActiveUserRoleRule(DenyAbortMixin, Rule):
    """
    Ensure that the current_user is activated.
    """

    def check(self):
        # Do not override DENY_ABORT_HTTP_CODE because inherited classes will
        # better use HTTP 403/Forbidden code on denial.
        self.DENY_ABORT_HTTP_CODE = response.Unauthorized.code
        # NOTE: `is_active` implies `is_authenticated`.
        return current_user.is_active


class PasswordRequiredRule(DenyAbortMixin, Rule):
    """
    Ensure that the current user has provided a correct password.
    """

    def __init__(self, password, **kwargs):
        super(PasswordRequiredRule, self).__init__(**kwargs)
        self._password = password

    def check(self):
        return current_user.password == self._password


class AdminRoleRule(ActiveUserRoleRule):
    """
    Ensure that the current_user has an Admin role.
    """

    def check(self):
        return current_user.is_admin


class InternalRoleRule(ActiveUserRoleRule):
    """
    Ensure that the current_user has an Internal role.
    """

    def check(self):
        return current_user.is_internal


class SupervisorRoleRule(ActiveUserRoleRule):
    """
    Ensure that the current_user has a Supervisor access to the given object.
    """

    def __init__(self, obj, **kwargs):
        super(SupervisorRoleRule, self).__init__(**kwargs)
        self._obj = obj

    def check(self):
        if not hasattr(self._obj, 'check_supervisor'):
            return False
        return self._obj.check_supervisor(current_user) is True


class OwnerRoleRule(ActiveUserRoleRule):
    """
    Ensure that the current_user has an Owner access to the given object.
    """

    def __init__(self, obj, **kwargs):
        super(OwnerRoleRule, self).__init__(**kwargs)
        self._obj = obj

    def check(self):
        if not hasattr(self._obj, 'check_owner'):
            return False
        return self._obj.check_owner(current_user) is True
