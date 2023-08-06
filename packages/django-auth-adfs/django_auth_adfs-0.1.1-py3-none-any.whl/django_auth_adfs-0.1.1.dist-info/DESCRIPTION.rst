ADFS Authentication for Django
==============================

.. image:: https://readthedocs.org/projects/django-auth-adfs/badge/?version=latest
    :target: http://django-auth-adfs.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://img.shields.io/pypi/v/django-auth-adfs.svg
    :target: https://pypi.python.org/pypi/django-auth-adfs
.. image:: https://travis-ci.org/jobec/django-auth-adfs.svg?branch=master
    :target: https://travis-ci.org/jobec/django-auth-adfs
.. image:: https://codecov.io/github/jobec/django-auth-adfs/coverage.svg?branch=master
    :target: https://codecov.io/github/jobec/django-auth-adfs?branch=master

A Django authentication backend for Microsoft ADFS

* Free software: BSD License
* Homepage: https://github.com/jobec/django-auth-adfs
* Documentation: http://django-auth-adfs.readthedocs.io/

Features
--------

* Integrates Django with Active Directory through Microsoft ADFS by using OAuth2.
* Provides seamless single sign on (SSO) for your Django project on intranet environments.
* Auto creates users and adds them to Django groups based on info in JWT claims received from ADFS.

Installation
------------

Python package::

    pip install django-auth-adfs

In your project's ``settings.py``

.. code-block:: python

    AUTHENTICATION_BACKENDS = (
        ...
        'django_auth_adfs.backend.AdfsBackend',
        ...
    )

    INSTALLED_APPS = (
        ...
        # Needed for the ADFS redirect URI to function
        'django_auth_adfs',
        ...

    # checkout config.py for more settings
    AUTH_ADFS = {
        "SERVER": "adfs.yourcompany.com",
        "CLIENT_ID": "your-configured-client-id",
        "RESOURCE": "your-adfs-RPT-name",
        # Make sure to read the documentation about the AUDIENCE setting
        # when you configured the identifier as a URL!
        "AUDIENCE": "microsoft:identityserver:your-RelyingPartyTrust-identifier",
        "ISSUER": "http://adfs.yourcompany.com/adfs/services/trust",
        "CA_BUNDLE": "/path/to/ca-bundle.pem",
        "CLAIM_MAPPING": {"first_name": "given_name",
                          "last_name": "family_name",
                          "email": "email"},
        "REDIR_URI": "https://www.yourcompany.com/oauth2/login",
    }

    ########################
    # OPTIONAL SETTINGS
    ########################
    TEMPLATES = [
        {
            ...
            'OPTIONS': {
                'context_processors': [
                    # Only needed if you want to use the variable ADFS_AUTH_URL in your templates
                    'django_auth_adfs.context_processors.adfs_url',
                    ...
                ],
            },
        },
    ]


    MIDDLEWARE_CLASSES = (
        ...
        # With this you can force a user to login without using
        # the @login_required decorator for every view function
        #
        # You can specify URLs for which login is not forced by
        # specifying them in LOGIN_EXEMPT_URLS in setting.py.
        # The values in LOGIN_EXEMPT_URLS are interpreted as regular expressions.
        'django_auth_adfs.middleware.LoginRequiredMiddleware',
    )

In your project's ``urls.py``

.. code-block:: python

    urlpatterns = [
        ...
        # Needed for the redirect URL to function
        # The namespace is important and shouldn't be changed
        url(r'^oauth2/', include('django_auth_adfs.urls', namespace='auth_adfs')),
        ...
    ]

The URL you have to configure as the redirect URL in ADFS depends on the url pattern you configure.
In the example above you have to make the redirect url in ADFS point to ``https://yoursite.com/oauth2/login``

Contributing
------------
Contributions to the code are more then welcome.
For more details have a look at the ``CONTRIBUTING.rst`` file.


Changelog
---------

0.1.1 (2016-12-13)
~~~~~~~~~~~~~~~~~~

* Numerous typos fixed in code and documentation.
* Proper handling of class variables to allow inheriting from the class `AdfsBackend`.

0.1.0 (2016-12-11)
~~~~~~~~~~~~~~~~~~

* By default, the ADFS signing certificate is loaded from the ``FederationMetadata.xml`` file every 24 hours.
  Allowing to automatically follow certificate updates when the ADFS settings for ``AutoCertificateRollover``
  is set to ``True`` (the default).
* Group assignment optimisation. Users are not removed and added to all groups anymore. Instead only the
  groups that need to be removed or added are handled.

**Backwards incompatible changes**

* The redundant ``ADFS_`` prefix was removed from the configuration variables.
* The ``REQUIRE_LOGIN_EXEMPT_URLS`` variable was renamed to ``LOGIN_EXEMPT_URLS``

0.0.5 (2016-12-10)
~~~~~~~~~~~~~~~~~~

* User update code in authentication backend split into separate functions.

0.0.4 (2016-03-14)
~~~~~~~~~~~~~~~~~~

* Made the absence of the group claim non-fatal to allow users without a group.

0.0.3 (2016-02-21)
~~~~~~~~~~~~~~~~~~

* ADFS_REDIR_URI is now a required setting
* Now supports Python 2.7, 3.4 and 3.5
* Now supports Django 1.7, 1.8 and 1.9
* Added debug logging to aid in troubleshooting
* Added unit tests
* Lot's of code cleanup

0.0.2 (2016-02-11)
~~~~~~~~~~~~~~~~~~

* Fixed a possible issue with the cryptography package when used with apache + mod_wsgi.
* Added a optional context processor to make the ADFS authentication URL available as a template variable (ADFS_AUTH_URL).
* Added a optional middleware class to be able force an anonymous user to authenticate.

0.0.1 (2016-02-09)
~~~~~~~~~~~~~~~~~~

* Initial release


