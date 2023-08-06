Panflute: Pythonic Pandoc Filters
=================================

|Python version| |PyPI version| |Development Status| |Build Status|

`panflute <http://scorreia.com/software/panflute/>`__ is a Python
package that makes creating Pandoc filters fun.

For a detailed user guide, documentation, and installation instructions,
see http://scorreia.com/software/panflute/ (or the `PDF
version <http://scorreia.com/software/panflute/Panflute.pdf>`__). If you
want to contribute, head `here </CONTRIBUTING.md>`__.

Install
-------

To install panflute, open the command line and type:

Python 3
~~~~~~~~

::

    pip install git+git://github.com/sergiocorreia/panflute.git

-  Requires Python 3.3 or later.
-  On windows, the command line (``cmd``) must be run as administrator.

Python 2
~~~~~~~~

::

    pip install git+git://github.com/sergiocorreia/panflute.git@python2

Note: see the related
`issue <https://github.com/sergiocorreia/panflute/issues/5>`__.

Uninstall
---------

::

    pip uninstall panflute

Dev Install
-----------

After cloning the repo and opening the panflute folder:

``python setup.py install``
    installs the package locally
``python setup.py develop``
    installs locally with a symlink so changes are automatically updated

Contributing
------------

Feel free to submit push requests. For consistency, code should comply
with `pep8 <https://pypi.python.org/pypi/pep8>`__ (as long as its
reasonable), and with the style guides by
[@kennethreitz](http://docs.python-guide.org/en/latest/writing/style/)
and `google <http://google.github.io/styleguide/pyguide.html>`__. Read
more `here </CONTRIBUTING.md>`__.

License
-------

BSD3 license (following ``pandocfilters`` by @jgm).

.. |Python version| image:: https://img.shields.io/pypi/pyversions/panflute.svg
   :target: https://pypi.python.org/pypi/panflute/
.. |PyPI version| image:: https://img.shields.io/pypi/v/panflute.svg
   :target: https://pypi.python.org/pypi/panflute/
.. |Development Status| image:: https://img.shields.io/pypi/status/panflute.svg
   :target: https://pypi.python.org/pypi/panflute/
.. |Build Status| image:: https://travis-ci.org/sergiocorreia/panflute.svg?branch=master
   :target: https://travis-ci.org/sergiocorreia/panflute
