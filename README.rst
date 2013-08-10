Pyramid authentication stack
============================

.. image:: https://travis-ci.org/wichert/pyramid_authstack.png?branch=master
    :target: https://travis-ci.org/wichert/pyramid_authstack

The `pyramid_authstack` package makes it possible to stack multiple
authentication policies in a `pyramid <http://www.pylonsproject.org>`_ project.
This can be useful in several scenarios:

- You need to be able to identify a user for a long period of time, while
  requiting a recent login to access personal information. Amazon is an
  example of a site doing this.

- You want to send a newsletter to users and log the user in automatically when
  they follow a link in the newsletter, but not give automatically give them
  access to sensitive information.

Confusing a multi-authentication policy is simple: create an instance
of the `MultiAuthenticationPolicy` object, add the authentication policies
you want to it and then tell Pyramid to use it.

::

    from pyramid.authentication import AuthTktAuthenticationPolicy
    from pyramid_authstack import MultiAuthenticationPolicy

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


Comparison to pyramid_multiauth
===============================

Mozilla has a similar project: `pyramid_multiauth
<https://pypi.python.org/pypi/pyramid_multiauth>`_. There are a few difference
between that package and this one:

* pyramid_multiauth has no way to indicate which authentication policy matched,
  which makes it unusable for my uses causes unless you always use custom
  authentication sub-policies which add custom an extra principal.  This could
  be fixed, but it would require changing the API in a non-backward compatible
  way.
* pyramid_multiauth duplicates some of the callback-handling code instead of
  reusing pyramid's CallbackAuthenticationPolicy.
* pyramid_multiauth allows configuration via the PasteDeploy .ini file, which
  pyramid_authstack does not support.


Changelog
=========

1.0.0 - August 10, 2013
-----------------------

- First release.
