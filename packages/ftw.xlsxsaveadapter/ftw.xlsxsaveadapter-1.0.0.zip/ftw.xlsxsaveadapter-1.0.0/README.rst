.. contents:: Table of Contents


Introduction
============


This package adds an excel save adapter for PloneFormGen.
The adapter is derived from the existing csv adapter and adds options
to either download an excel through the site or email the excel file to a list of recipients.

Compatibility
-------------

Plone 4.3.x


Installation
============

- Add the package to your buildout configuration:

::

    [instance]
    eggs +=
        ...
        ftw.xlsxsaveadapter


Development
===========

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buildout.cfg``
4. Shell: ``python bootstrap.py``
5. Shell: ``bin/buildout``

Run ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.


Links
=====

- Github: https://github.com/4teamwork/ftw.xlsxsaveadapter
- Issues: https://github.com/4teamwork/ftw.xlsxsaveadapter/issues
- Pypi: http://pypi.python.org/pypi/ftw.xlsxsaveadapter


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.xlsxsaveadapter`` is licensed under GNU General Public License, version 2.
