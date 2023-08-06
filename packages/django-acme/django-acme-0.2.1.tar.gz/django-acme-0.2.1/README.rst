===========
Django ACME
===========

.. image:: https://badge.fury.io/py/django-acme.svg
    :target: https://badge.fury.io/py/django-acme

.. image:: https://travis-ci.org/browniebroke/django-acme.svg?branch=master
    :target: https://travis-ci.org/browniebroke/django-acme

.. image:: https://codecov.io/gh/browniebroke/django-acme/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/browniebroke/django-acme

A re-usable Django app to quickly deploy a page for the ACME challenge

Documentation
-------------

The full documentation is at https://django-acme.readthedocs.io.

Quickstart
----------

Install Django ACME::

    pip install django-acme

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'acme_challenge',
        ...
    )

Add the Django ACME's URL patterns:

.. code-block:: python
    
    from acme_challenge import urls as acme_challenge_urls


    urlpatterns = [
        ...
        url(r'^', include(acme_challenge_urls)),
        ...
    ]

The URL of the ACME challenge to serve as well as the content are
controlled via 2 settings which default to:

.. code-block:: python

    ACME_CHALLENGE_URL_SLUG = os.getenv('ACME_CHALLENGE_URL_SLUG')
    ACME_CHALLENGE_TEMPLATE_CONTENT = os.getenv('ACME_CHALLENGE_TEMPLATE_CONTENT')

The slug being the suffix of the URL path:
`/.well-known/acme-challenge/[ACME_CHALLENGE_URL_SLUG]/`

Features
--------

* TODO

Running Tests
-------------

Does the code actually work? This projects uses tox_:

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox [-e py27-django18]

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
.. _tox: https://tox.readthedocs.io/en/latest/
