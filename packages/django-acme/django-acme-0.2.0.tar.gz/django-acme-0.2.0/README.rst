=============================
Django ACME
=============================

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

Define these 2 settings:

.. code-block:: python

    ACME_CHALLENGE_URL_SLUG = os.getenv('ACME_CHALLENGE_URL_SLUG')
    ACME_CHALLENGE_TEMPLATE_CONTENT = os.getenv('ACME_CHALLENGE_TEMPLATE_CONTENT')

Add the Django ACME's URL patterns:

.. code-block:: python
    
    from acme_challenge import urls as acme_challenge_urls


    urlpatterns = [
        ...
        url(r'^', include(acme_challenge_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
