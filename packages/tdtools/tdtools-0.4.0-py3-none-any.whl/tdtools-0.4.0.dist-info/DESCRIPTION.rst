tdtools
=======

.. image:: https://img.shields.io/pypi/v/tdtools.svg
     :target: https://pypi.python.org/pypi/tdtools
     :alt: PyPi
.. image:: https://img.shields.io/badge/License-GPL%20-blue.svg
     :target: http://www.gnu.org/licenses/gpl
     :alt: License

`tdtools <https://bitbucket.org/padhia/tdtools>`_ is a collection of tools and utilities I developed for my personal use. I am making these tools open-source in the hope that someone else might find them useful.

*NOTE:* These tools are not endorsed by `Teradata Inc <http://www.teradata.com/>`_.

Requirements
------------

Theses tools are tested with Python 3.4 and Python 3.5. Python 2.7 version isn't part of the test and most likely will not work. However, if there is a strong interest in using Python 2.7 and changes required to support Python 2.7 are minimal, I may consider making selected modules support Python 2.7.

There is a dependency on `teradata <https://pypi.python.org/pypi/teradata/>`_ python package. It'll be downloaded automatically if you use standard python installer ``pip``.

Installation
------------

Use Python's standard ``pip`` utility to install ``tdtools``. Although ``tdtools`` doesn't have too many dependecies, you may choose to install in an ``virtualenv``.::

  $ pip install tdtools

Or

  C:\>python -m pip install tdtools

Configuration
-------------

No configuration is required except setting up the needed ODBC connections. All scripts that are part of ``tdtools`` accept arbitrary ``ODBC`` connection strings using ``--tdconn`` parameter.

If more flexibility is needed, for example, to use Teradata REST APIs, it may be done by providing ``sqlcsr_site.py`` in your ``PYTHONPATH``. Have a look at ``sqlcsr.py`` module to get an idea about what can be overriden in ``sqlcsr_site.py``.

Tools
-----

All tools are command-line utilities that are automatically installed when ``tdtools`` is installed using ``pip``. What follows is a brief description of each tool. Each tool support ``--help`` or ``-h`` command-line option that shows detailed description of options supported.

* ``dbtree``: Prints Teradata database hierarchy.
* ``vwtree``: Prints (or save) view hierarchy.
* ``tptload``: Generate (and optionally run on Linux) TPT load script.

All **show\*** utilities generate DDLs for different types of Teradata objects.

* ``showdb``: Teradata database or user
* ``showgrant``: Teradata grants to user/role
* ``showprof``: Teradata profile
* ``showrole``: Teradata role
* ``showtvm``: Wrapper around Teradata ``SHOW <object>`` command
* ``showzone``: Teradata zone

All **ls\*** utilities print Teradata object information from DBC tables. Currently supported commands are:

* ``lstb``: Tables
* ``lsvw``: Views
* ``lspr``: Stored Procedures
* ``lsji``: Join Indexes

Support:
--------

If you encounter an issue, report it using `issue tracker <https://bitbucket.org/padhia/tdtools/issues?status=new&status=open>`_. I'll try to provide a fix as soon as I can. If you already have a fix, send me a pull request.

Contributions:
--------------

Feel free to fork this repository and enhance it in a way you see fit. If you think your changes will benefit more people, send me a pull request.


