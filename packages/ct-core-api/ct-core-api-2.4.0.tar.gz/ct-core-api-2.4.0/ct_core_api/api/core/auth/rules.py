from permission import Rule as BaseRule

from ct_core_api.api.core import response


class DenyAbortMixin(object):
    """
    A helper permissions mixin raising an HTTP Error (specified in
    ``DENY_ABORT_CODE``) on deny.

    NOTE: Apply this mixin before Rule class so it can override NotImplemented
    deny method.
    """

    DENY_ABORT_HTTP_CODE = response.Forbidden.code
    DENY_ABORT_MESSAGE = None

    def deny(self):
        """
        Abort HTTP request by raising HTTP error exception with a specified
        HTTP code.
        """
        return response.abort(code=self.DENY_ABORT_HTTP_CODE, message=self.DENY_ABORT_MESSAGE)


class Rule(BaseRule):
    """
    Experimental base Rule class that helps to automatically handle inherited
    rules.
    """

    def base(self):
        # XXX: it handles only the first appropriate Rule base class
        # TODO: PR this case to permission project
        for base_class in self.__class__.__bases__:
            if issubclass(base_class, Rule):
                if base_class in {Rule, BaseRule}:
                    continue
                return base_class()


class AllowAllRule(Rule):
    """
    Helper rule that always grants access.
    """

    def check(self):
        return True


class PartialPermissionDeniedRule(Rule):
    """
    Helper rule that must fail on every check since it should never be checked.
    """

    def check(self):
        raise RuntimeError("Partial permissions are not intended to be checked")
