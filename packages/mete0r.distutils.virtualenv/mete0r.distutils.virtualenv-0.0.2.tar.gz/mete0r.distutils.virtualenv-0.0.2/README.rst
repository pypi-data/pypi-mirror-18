mete0r.distutils.virtualenv
===========================

Provides `virtualenv`_ management commands in your project's ``setup.py``.


.. _virtualenv: https://virtualenv.pypa.io


Setup
-----

In your setup.py::

   setup(
      name='FooPackage',
      ...
      setup_requires=[
         'mete0r.distutils.virtualenv',
      ],
      ...
   )


Commands
--------

=============================== =============================================================
Command                         Description
------------------------------- -------------------------------------------------------------
``virtualenv``                  Create a virtualenv environment.
``virtualenv_bootstrap_script`` Create a virtualenv bootstrap script. (`Experimental`)
``pip_sync``                    Synchronize the environment packages with a requirement file.
``pip_compile``                 Compile a requirement file.
=============================== =============================================================

For detailed usage::

   python setup.py virtualenv --help
   python setup.py virtualenv_bootstrap_script --help
   python setup.py pip_sync --help
   python setup.py pip_compile --help


Development environment
-----------------------

To setup development environment::

   python setup.py virtualenv
   make


License
-------

Copyright (C) 2015-2016 mete0r <mete0r@sarangbang.or.kr>

.. image:: https://www.gnu.org/graphics/lgplv3-147x51.png

`GNU Lesser General Public License v3.0 <http://www.gnu.org/licenses/lgpl-3.0.html>`_
`(text version) <http://www.gnu.org/licenses/lgpl-3.0.txt>`_

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
