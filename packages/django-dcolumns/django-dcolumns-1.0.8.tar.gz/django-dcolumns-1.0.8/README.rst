====================================
Django Tool to Create Dynamic Fields
====================================

.. image:: http://img.shields.io/pypi/v/django-dcolumns.svg
   :target: https://pypi.python.org/pypi/django-dcolumns
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/django-dcolumns.svg
   :target: https://pypi.python.org/pypi/django-dcolumns
   :alt: PY Versions

.. image:: http://img.shields.io/travis/cnobile2012/dcolumn/master.svg
   :target: http://travis-ci.org/cnobile2012/dcolumn
   :alt: Build Status

.. image:: http://img.shields.io/coveralls/cnobile2012/dcolumn/master.svg
   :target: https://coveralls.io/r/cnobile2012/dcolumn
   :alt: Test Coverage

.. image:: https://img.shields.io/pypi/dm/django-dcolumns.svg
   :target: https://pypi.python.org/pypi/django-dcolumns
   :alt: PyPI Downloads

The MIT License (MIT)

Overview
--------

At the time of this writing **DColumn** supports Django 1.10.1 and probably
back to 1.8.0. The biggest issue with supporting older versions of Django
is with the new way *urlpatterns* is used. Python 2.7, 3.4, 3.5 and 3.5-dev
are supported.

DColumn is a Django plugin that lets the developer add columns to a model
dynamically. It does this in the same way that the admin uses an inline model.
Matter-of-fact that is exactly how the additional columns are displayed in
the admin. The only addition is that there is special JavaScript that
converts the column type to the type you have previously set it to.

This can be done, because any type of field can be represented as a string.
There are two methods on any model you define as a **Dcolumn** model that
does conversion in and out of the type you have set.

.. warning::
   Version 1.0 is a complete rewrite of **Django DColumns** and is NOT
   backwards compatible with previous versions.

Provides
--------

1. Functionality to permit the addition of fields to a model through the admin.

2. Add quasi models for static data objects.

3. The admin reflects all newly added fields in the correct type.


Feel free to contact me at: carl dot nobile at gmail.com

Complete Documentation can be found on
`Read the Docs <https://readthedocs.org/>`_ at:
`Django DColumns <http://django-dcolumns.readthedocs.io/en/latest/>`_
