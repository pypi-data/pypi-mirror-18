mete0r.monkeypatchbuildout
==========================

monkeypatch `zc.buildout`_ for some reason

.. _zc.buildout: https://pypi.python.org/pypi/zc.buildout


Usage
-----

In your ``buildout.cfg``::

   [buildout]
   ...
   extensions =
      mete0r.monkeypatchbuildout


Development environment
-----------------------

To setup development environment::

   python setup.py virtualenv
   make
