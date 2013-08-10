Pyramid multi-authentication
============================

The `pyramid_multiauth` package makes it possible to use multiple authentication
policy in a `pyramid <http://www.pylonsproject.org>`_ project. This can be useful
in environment where you may nee to be able to identify a user for a long period,
while a recent login to access personal information.

::

    from pyramid.authentication import AuthTktAuthenticationPolicy
    from pyramid_multiauth import MultiAuthenticationPolicy

    auth_policy = MultiAuthenticationPolicy()
    # Add an authentication policy with a one-hour timeout to control
    # access to sensitive information.
    auth_policy.add_policy(
        'sensitive',
        AuthTktAuthenticationPolicy('secret', timeout=60 * 60))
    # Add a second authentication policy with a one-year timeout so
    # we can identify the user.
    auth_policy.add_policy(
        'identity',
        AuthTktAuthenticationPolicy('secret', timeout=60 * 60 * 24 * 365))
    config.set_authentication_policy(auth_policy)

The name used for the sub-policy (`sensitive` and `identity` in the example
above) will be added to the principals if the sub-policy can authenticate the
user. This makes it very easy to check which authentication policies matched
in an ACL::

    class MyModel(object):
        # Only allow access if user authenticated recently.
        __acl__ = [(Allow, 'auth:sensitive', 'view')]


When you call `remember()
<http://docs.pylonsproject.org/projects/pyramid/en/1.4-branch/api/security.html#pyramid.security.remember>`_ or `forget()
<http://docs.pylonsproject.org/projects/pyramid/en/1.4-branch/api/security.html#pyramid.security.forget>`_ all sub-policies will be trigged. You can filter the list
of policies used by adding a `policies` parameter. A use case where this
is important is a user coming to the site via a link in a newsletter: in
that scenario you can identify the user, but do not want to give access
to sensitive information without asking for extra credentials.

::

   from pyramid.security import remember

   # Only set identity-authentication.
   headers = remember(request, 'chrism', policies=['identity'])
