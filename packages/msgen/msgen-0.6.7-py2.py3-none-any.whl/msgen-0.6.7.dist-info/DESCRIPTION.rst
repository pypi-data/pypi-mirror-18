msgen
========
Microsoft Genomics Command-line Client

Installation
------------
`msgen`_ is on PyPI and can be installed via:

::

  pip install msgen

msgen is compatible with Python 2.7 and 3.3+. To install for Python 3, some
distributions may use ``pip3`` instead. If you do not want to install msgen
as a system-wide binary and modify system-wide python packages, use the
``--user`` flag with ``pip`` or ``pip3``.

- Base Requirements

  - `azure-storage`_
  - `requests`_


You can install these packages using pip, easy_install or through standard
setup.py procedures. These dependencies will be automatically installed if
using a package-based install or setup.py. The required versions of these
dependent packages can be found in ``setup.py``.

.. _azure-storage: https://pypi.python.org/pypi/azure-storage
.. _requests: https://pypi.python.org/pypi/requests

Introduction
------------

The msgen.py script is the Microsoft Genomics Command-line Client.

Example Usage
-------------

::

  msgen -f ~/msgen.config.txt

Note: You'll need to create a file with your configuration details. In this
example it is ``~/msgen.config.txt``.

