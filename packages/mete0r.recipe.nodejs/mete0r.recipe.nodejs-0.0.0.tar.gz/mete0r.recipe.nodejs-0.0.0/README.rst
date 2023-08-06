mete0r.recipe.nodejs
====================

a `zc.buildout`_ recipe to install `node.js`_

.. _zc.buildout: https://pypi.python.org/pypi/zc.buildout
.. _node.js: https://nodejs.org


Quickstart
----------

In your buildout.cfg::

   [buildout]
   parts =
      nodejs

   [nodejs]
   recipe = mete0r.recipe.nodejs
   version = v6.9.1


``node``, ``npm`` will be installed in ``${buildout:bin-directory}``.


Limitation
----------

Currently supports ``Linux`` and ``Darwin`` only. (``platform.system()``)


Development environment
-----------------------

To setup development environment::

   python setup.py virtualenv
   make
   bin/buildout
