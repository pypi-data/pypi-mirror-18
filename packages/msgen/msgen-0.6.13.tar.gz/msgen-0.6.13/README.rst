msgen
========
Microsoft Genomics Command-line Client

Installation
------------
`msgen`_ is on PyPI and can be installed via:

Linux

::

  sudo apt-get install -y build-essential libssl-dev libffi-dev libpython-dev python-dev python-pip
  sudo pip install --upgrade --no-deps msgen
  sudo pip install msgen

Windows

::

  pip install --upgrade --no-deps msgen
  pip install msgen


msgen is compatible with Python 2.7. If you do not want to install msgen
as a system-wide binary and modify system-wide python packages, use the
``--user`` flag with ``pip``.

- Base Requirements

  - `azure-storage`_
  - `requests`_


You can install these packages using pip, easy_install or through standard
setup.py procedures. These dependencies will be automatically installed if
using a package-based install or setup.py. The required versions of these
dependent packages can be found in ``setup.py``.

.. _azure-storage: https://pypi.python.org/pypi/azure-storage
.. _requests: https://pypi.python.org/pypi/requests

Description
------------

The msgen.py script is the Microsoft Genomics Command-line Client.

Example Usage
-------------

::

  msgen -f ~/msgen.config.txt

Note: You'll need to create a file with your configuration details. In this
example it is ``~/msgen.config.txt``.

