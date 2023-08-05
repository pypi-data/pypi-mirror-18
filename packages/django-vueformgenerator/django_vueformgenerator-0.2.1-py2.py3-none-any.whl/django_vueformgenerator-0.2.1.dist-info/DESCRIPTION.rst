=============================
Django-VueFormGenerator
=============================

.. image:: https://badge.fury.io/py/django-vueformgenerator.png
    :target: https://badge.fury.io/py/django-vueformgenerator

.. image:: https://travis-ci.org/player1537/django-vueformgenerator.png?branch=master
    :target: https://travis-ci.org/player1537/django-vueformgenerator

A package to help bridge the gap between Django's Forms and VueFormGenerator's Schemas using DjangoRestFramework.

Documentation
-------------

The full documentation is at https://django-vueformgenerator.readthedocs.org.

Quickstart
----------

Install Django-VueFormGenerator::

    pip install django-vueformgenerator

Then use it in a project::

    from django_vueformgenerator.schema import Schema
    from django import forms
    import json

    class TestForm(forms.Form):
        title = forms.CharField(max_length=128)
        content = forms.TextField(max_length=1280)

    form = TestForm()  # or TestForm(data={'title':'My Title'})
    schema = Schema().render(form)
    print(json.dumps(schema))


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




History
-------

0.1.0 (2016-10-11)
++++++++++++++++++

* First release on PyPI.

0.1.1 (2016-10-18)
++++++++++++++++++

* Add additional tests for schema generation
* Add components for numbers and for selecting between choices
* Add Python 2 support
* Add better documentation
* Fix exception raised on bad widget

0.2.0 (2016-10-25)
++++++++++++++++++

* Add ability to use existing data in form
* DEPRECATED: Any code which previously used `Schema().render(MyForm)` should
  now use `Schema().render(MyForm())` (in other words, `render()` accepts an
  instance of a form, rather than a form itself). To check if you are calling
  the function against contract, you can run your code with `python -Wd`
  (e.g. `python -Wd manage.py runserver`).

0.2.1 (2016-10-27)
++++++++++++++++++

* Fix bug in tests so that the tests run successfully in Python 2.7.


