Django Cryptography
===================

A set of primitives for easily encrypting data in Django, wrapping
the Python Cryptography_ library. Also provided is a drop in
replacement for Django's own cryptographic primitives, using
Cryptography_ as the backend provider.

Do not forget to read the documentation_.

.. image:: https://img.shields.io/travis/georgemarshall/django-cryptography/stable/0.2.x.svg
   :target: https://travis-ci.org/georgemarshall/django-cryptography
   :alt: Builds
.. image:: https://img.shields.io/codecov/c/github/georgemarshall/django-cryptography/stable/0.2.x.svg
   :target: https://codecov.io/gh/georgemarshall/django-cryptography/branch/stable%2F0.2.x
   :alt: Code coverage
.. image:: https://www.quantifiedcode.com/api/v1/project/ceb16c3d35264fd0a1be165af1456d4e/snapshot/origin:stable:0.2.x:HEAD/badge.svg
   :target: https://www.quantifiedcode.com/app/project/ceb16c3d35264fd0a1be165af1456d4e?branch=origin%2Fstable%2F0.2.x
   :alt: Code issues

Cryptography by example
-----------------------

Using symmetrical encryption to store sensitive data in the database.
Wrap the desired model field with ``encrypt`` to easily
protect its contents.

.. code-block:: python

   from django.db import models

   from django_cryptography.fields import encrypt


   class MyModel(models.Model):
       name = models.CharField(max_length=50)
       sensitive_data = encrypt(models.CharField(max_length=50))

The data will now be automatically encrypted when saved to the
database.  ``encrypt`` uses an encryption that allows for
bi-directional data retrieval.

Requirements
------------

* Python_ (2.7, 3.3, 3.4 or 3.5)
* Cryptography_ (1.3)
* Django_ (1.8 or 1.9)

Installation
------------

.. code-block:: console

   pip install django-cryptography

.. _Cryptography: https://cryptography.io/
.. _Django: https://www.djangoproject.com/
.. _Python: https://www.python.org/
.. _documentation: https://django-cryptography.readthedocs.io/en/stable-0.2.x/
