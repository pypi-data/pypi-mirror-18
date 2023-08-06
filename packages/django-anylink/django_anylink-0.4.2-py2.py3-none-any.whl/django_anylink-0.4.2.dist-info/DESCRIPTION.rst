==========================
Generic linking for Django
==========================

.. image:: https://badge.fury.io/py/django-anylink.png
    :target: http://badge.fury.io/py/django-anylink
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/moccu/django-anylink.png
   :target: https://travis-ci.org/moccu/django-anylink
   :alt: Latest Travis CI build status

.. image:: https://coveralls.io/repos/moccu/django-anylink/badge.svg
  :target: https://coveralls.io/github/moccu/django-anylink
  :alt: Coverage of master build

.. image:: https://readthedocs.org/projects/django-anylink/badge/?version=latest
    :target: https://readthedocs.org/projects/django-anylink/?badge=latest
    :alt: Latest read the docs build


`django-anylink` is a generic linking module for Django. Using this module, you
can create links for many usecases.


Installation & Documentation
----------------------------

You can find all documentation in the "docs/source" folder and online at
All documentation is in the "docs/source" directory and online at
`Read the Docs <https://readthedocs.org/projects/django-anylink/>`_.


License
-------

*django-anylink* is licenced under the BSD License (see LICENSE).


Resources
---------

* `Documentation <https://readthedocs.org/projects/django-anylink/>`_
* `Bug Tracker <https://github.com/moccu/django-anylink/issues/>`_
* `Code <https://github.com/moccu/django-anylink>`_


Changes
=======

0.4.2 (2016-11-24)
------------------

* Fix AddOrChangeWidget for Django 1.9

0.4.1 (2016-10-04)
------------------

* Fix translation
* Improve message formatting for multi link warning
* Order link_type choices alphabetically to avoid redundant migrations
* Update documentation


0.4.0 (2016-05-11)
------------------

* Add support for django 1.9
* Use SVG if django-version is greater than 1.8


0.3.0 (2015-09-22)
------------------

* Add support for django 1.8 and python3.5
* drop support for django 1.5


0.2.0 (2015-03-30)
------------------

* Integrate Travis CI.
* Allow customization of admin form.
* Ensure the admin widget is not recognized as hidden input.
* Add ``ANYLINK_ALLOW_MULTIPLE_USE`` setting to enable reusability of AnyLink objects.
* We don't check Python 3.3 anymore.
* Added Dutch and German translations.


0.1.0 (2014-06-17)
------------------

* Initial release for the public.

Contains the following features:

* Generic linking in Django
* Support for TinyMCE
* Supports Python 2.7, 3.3, 3.4, PyPy and Django 1.5+


