===============
formatflowed.py
===============

Introduction
------------

The formatflowed.py python library provides en- and decoding functionality for 
`RFC 2646`_ and `RFC 3676`_ text, also called format=flowed text. The 
development of this library was generously sponsored by `Logicalware`_, and
was written by `Martijn Pieters <mj@zopatista.com>`_.

The latest version can be downloaded from the `pypi page`_; the code repository 
is hosted `GitHub`_.

.. image:: https://travis-ci.org/mjpieters/formatflowed.svg?branch=master
    :target: https://travis-ci.org/mjpieters/formatflowed

.. _RFC 2646: http://www.faqs.org/rfcs/rfc2646.html
.. _RFC 3676: http://www.faqs.org/rfcs/rfc3676.html
.. _Logicalware: http://www.logicalware.com/
.. _pypi page: http://pypi.python.org/pypi/formatflowed
.. _GitHub: https://github.com/mjpieters/formatflowed


Requirements
------------

formatflowed.py has been tested with python versions 2.6 - 2.7, 3.3 - 3.6 and
pypy and pypy3. Installation requires setuptools.


Installation
------------

Use the standard setuptools installation script provided::

 python setup.py install

or install the package as an egg::

 pip install formatflowed 


Usage
-----

Further documentation is embedded in the docstrings of the module.


Change History
==============

2.0.0 (2016-11-29)
------------------

* Dropped support for Python < 2.6
* Cleaned up bytes vs. unicode handling to be consistent
* Added official support for Python >= 3.3 and PyPy.

1.1.0 (2012-03-15)
------------------

* Made unicode exception handling configurable.
  [mj]

* Updated project URLs, and cleaned up setup.py. The project is now hosted on
  GitHub.
  [mj]

1.0.0 (2005-09-17)
------------------

* Added release metadata and a README.
  [mj]

0.9.0 (2005-09-11)
------------------

* Initial release.
  [mj]


