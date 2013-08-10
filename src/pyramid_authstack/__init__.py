import collections
from zope.interface import implementer
from pyramid.authentication import Authenticated
from pyramid.authentication import Everyone
from pyramid.authentication import IAuthenticationPolicy
from pyramid.authentication import CallbackAuthenticationPolicy


@implementer(IAuthenticationPolicy)
class AuthenticationStackPolicy(CallbackAuthenticationPolicy):
    def __init__(self, callback=None):
        self.callback = callback
        self.policies = collections.OrderedDict()

    def add_policy(self, name, policy):
        self.policies[name] = policy

    def unauthenticated_userid(self, request):
        for policy in self.policies.values():
            userid = policy.unauthenticated_userid(request)
            if userid is not None:
                return userid
        else:
            return None

    def effective_principals(self, request):
        principals = set([Everyone])
        for (name, policy) in self.policies.items():
            new_principals = policy.effective_principals(request)
            principals.update(new_principals)
            if Authenticated in new_principals:
                principals.add('auth:%s' % name)
        return list(principals)

    def remember(self, request, principal, policies=None, **kw):
        headers = []
        for (name, policy) in self.policies.items():
            if policies is None or name in policies:
                headers.extend(policy.remember(request, principal, **kw))
        return headers

    def forget(self, request, policies=None):
        headers = []
        for (name, policy) in self.policies.items():
            if policies is None or name in policies:
                headers.extend(policy.forget(request))
        return headers
