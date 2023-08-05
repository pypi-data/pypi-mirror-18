django-mustache
===============

A straightforward Mustache-powered template engine for Django, extracted
from `wq.db <https://wq.io/wq.db/>`__ and updated to support the new
`template
backend <https://docs.djangoproject.com/en/1.10/topics/templates>`__
infrastructure in Django 1.8 and newer. *django-mustache* facilitates
`progressive enhancement <https://wq.io/docs/website>`__ by allowing you
to share the same templates between Django and an offline-capable
JavaScript `web app <https://wq.io/docs/web-app>`__. Combined with a
shared `URL structure <https://wq.io/docs/url-structure>`__, this
approach ensures that each page in your site can be selectively rendered
on the `server or on the client <https://wq.io/docs/templates>`__ as
needed.

A number of Pystache/Mustache backends for Django exist, though many are
outdated. Only this library provides all of the following:

-  Full integration with existing Django context processors like
   ``django.template.context_processors.csrf`` and
   ``django.contrib.auth.context_processors.auth``.\*
-  Full test suite
-  Installable via PyPI
-  Compatible with Django 1.8 and newer

    \*\ `wq/app.js <https://wq.io/docs/app-js>`__ provides client-side
    equivalents for these context variables.

|Latest PyPI Release| |Release Notes| |License| |GitHub Stars| |GitHub
Forks| |GitHub Issues|

|Travis Build Status| |Python Support| |Django Support|

Usage
~~~~~

.. code:: bash

    pip3 install django-mustache

Configure django-mustache like you would any `template
backend <https://docs.djangoproject.com/en/1.10/topics/templates>`__:

.. code:: python

    # myproject/settings.py
    TEMPLATES = [
        {
            'BACKEND': 'django_mustache.Mustache',
            'DIRS': [ '...' ],
            'APP_DIRS': False,
            'OPTIONS': {
                'context_processors': [ '...' ],
                'partials_dir': 'partials',
                'file_extension': 'html',
            }
        },
        # ...
    ]

The following configuration options are supported:

-  **context\_processors**: equivalent to the Django template backend
   setting. The goal is to be able to use the same context processors
   for both Django and Mustache template backends. (Let us know if you
   come across any compatibility issues.)
-  **partials\_dir**: If set, django-mustache will check each template
   directory for a subfolder containing Mustache partial templates. The
   default partial folder name is 'partials'. Set to ``False`` to
   disable this feature.
-  **file\_extension**: File extension to use when searching for
   templates and partials. The default is '.html', which should not
   conflict with existing Django templates as long as completely
   separate directories are configured for Mustache templates. Django
   views typically include the extension in the template name - this is
   taken into account when searching for templates.

.. |Latest PyPI Release| image:: https://img.shields.io/pypi/v/django-mustache.svg
   :target: https://pypi.python.org/pypi/django-mustache
.. |Release Notes| image:: https://img.shields.io/github/release/wq/django-mustache.svg
   :target: https://github.com/wq/django-mustache/releases
.. |License| image:: https://img.shields.io/pypi/l/django-mustache.svg
   :target: https://github.com/wq/django-mustache/blob/master/LICENSE
.. |GitHub Stars| image:: https://img.shields.io/github/stars/wq/django-mustache.svg
   :target: https://github.com/wq/django-mustache/stargazers
.. |GitHub Forks| image:: https://img.shields.io/github/forks/wq/django-mustache.svg
   :target: https://github.com/wq/django-mustache/network
.. |GitHub Issues| image:: https://img.shields.io/github/issues/wq/django-mustache.svg
   :target: https://github.com/wq/django-mustache/issues
.. |Travis Build Status| image:: https://img.shields.io/travis/wq/django-mustache/master.svg
   :target: https://travis-ci.org/wq/django-mustache
.. |Python Support| image:: https://img.shields.io/pypi/pyversions/django-mustache.svg
   :target: https://pypi.python.org/pypi/django-mustache
.. |Django Support| image:: https://img.shields.io/badge/Django-1.8%2C%201.9%2C%201.10-blue.svg
   :target: https://pypi.python.org/pypi/django-mustache
