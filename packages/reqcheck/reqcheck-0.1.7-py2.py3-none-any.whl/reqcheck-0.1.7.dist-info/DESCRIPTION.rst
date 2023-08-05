reqcheck
========

.. image:: https://img.shields.io/pypi/v/reqcheck.svg
    :target: https://pypi.python.org/pypi/reqcheck
    :alt: Latest Version

.. image:: https://travis-ci.org/jaleskovec/reqcheck.svg?branch=master
    :target: https://travis-ci.org/jaleskovec/reqcheck

.. image:: https://coveralls.io/repos/github/jaleskovec/reqcheck/badge.svg
    :target: https://coveralls.io/github/jaleskovec/reqcheck

Compare installed Python package versions with PyPI. Display the current
version, latest version and age for each installed package.

Example output:

::

      Package        Current Version    Latest Version    Age
      -------------  -----------------  ----------------  -------------------------------
      BeautifulSoup  3.2.0              3.2.1             -1 version (~ 1 year 86 days)
      funcsigs       1.0.2              1.0.2             latest
      mock           2.0.0              2.0.0             latest
      pbr            1.10.0             1.10.0            latest
      requests       2.9.1              2.11.1            -4 versions (~ 240 days)
      six            1.10.0             1.10.0            latest
      wheel          0.24.0             0.30.0a0          -6 versions (~ 2 years 71 days)

Installation
------------

To install reqcheck, simply use pip:

::

    $ pip install reqcheck

Usage
-----

You can check requirements directly using stdin:

::

    $ pip freeze | reqcheck

You can check requirements in a virtualenv:

::

    $ reqcheck -v /path/to/venv

You can check requirements on the command line:

::

    $ reqcheck requests==2.10.0 mock==2.0.0

Display usage help:

::

    $ reqcheck --help

Contributing
------------

1. Check the pull requests to ensure that your feature hasn't been
   requested already
2. Fork the repository and make your changes in a separate branch
3. Add unit tests for your changes
4. Submit a pull request
5. Contact the maintainer


