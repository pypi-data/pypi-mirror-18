**Django Data Wizard** is a `wq-powered <https://wq.io/>`__ web-based
tool for mapping structured data (e.g. Excel, XML) into a highly
normalized database structure via Django. The current implementation
relies heavily on the `ERAV <https://wq.io/docs/erav>`__ implementation
provided by `vera <https://wq.io/vera>`__, though there are plans to
extend this to support any database structure
(`#3 <https://github.com/wq/django-data-wizard/issues/3>`__).

The unique feature of Django Data Wizard is that it allows novice users
to map spreadsheet columns to database fields (and cell values to
foreign keys) on-the-fly during the import process. This reduces the
need for preset spreadsheet formats, which most data import solutions
require.

Django Data Wizard supports any format supported by
`wq.io <https://wq.io/wq.io>`__. Additional formats can be integrating
by creating a `custom wq.io class <https://wq.io/docs/custom-io>`__ and
then registering it with the wizard. For example, the `Climata
Viewer <https://github.com/heigeo/climata-viewer>`__ uses Django Data
Wizard to import data from
`climata <https://github.com/heigeo/climata>`__'s wq.io-based data
loaders.

    *Note:* Django Data Wizard was formerly known as the **dbio**
    contrib module in `wq.db <https://wq.io/wq.db>`__. The
    implementation has been extracted from wq.db and renamed to avoid
    confusion with other similar libraries.

|Latest PyPI Release| |Release Notes| |License| |GitHub Stars| |GitHub
Forks| |GitHub Issues|

|Travis Build Status| |Python Support| |Django Support|

Getting Started
===============

.. code:: bash

    pip3 install data-wizard

Django Data Wizard is an extension to `wq.db <https://wq.io/wq.db>`__,
the database component of the `wq framework <https://wq.io/>`__. See
https://github.com/wq/django-data-wizard to report any issues.

Examples
========

|Climata Viewer|

|river.watch|

.. |Latest PyPI Release| image:: https://img.shields.io/pypi/v/data-wizard.svg
   :target: https://pypi.python.org/pypi/data-wizard
.. |Release Notes| image:: https://img.shields.io/github/release/wq/django-data-wizard.svg
   :target: https://github.com/wq/django-data-wizard/releases
.. |License| image:: https://img.shields.io/pypi/l/data-wizard.svg
   :target: https://wq.io/license
.. |GitHub Stars| image:: https://img.shields.io/github/stars/wq/django-data-wizard.svg
   :target: https://github.com/wq/django-data-wizard/stargazers
.. |GitHub Forks| image:: https://img.shields.io/github/forks/wq/django-data-wizard.svg
   :target: https://github.com/wq/django-data-wizard/network
.. |GitHub Issues| image:: https://img.shields.io/github/issues/wq/django-data-wizard.svg
   :target: https://github.com/wq/django-data-wizard/issues
.. |Travis Build Status| image:: https://img.shields.io/travis/wq/django-data-wizard.svg
   :target: https://travis-ci.org/wq/django-data-wizard
.. |Python Support| image:: https://img.shields.io/pypi/pyversions/data-wizard.svg
   :target: https://pypi.python.org/pypi/data-wizard
.. |Django Support| image:: https://img.shields.io/badge/Django-1.8%2C%201.9%2C%201.10-blue.svg
   :target: https://pypi.python.org/pypi/data-wizard
.. |Climata Viewer| image:: https://wq.io/media/700/screenshots/climata-02.png
   :target: https://wq.io/projects/climata
.. |river.watch| image:: https://wq.io/media/700/screenshots/riverwatch-overview.png
   :target: https://wq.io/projects/river-watch
