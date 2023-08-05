==============================
pyems - Python EMS API wrapper
==============================

.. image:: https://codeclimate.com/github/tomi77/pyems/badges/gpa.svg
   :target: https://codeclimate.com/github/tomi77/pyems
   :alt: Code Climate
.. image:: https://travis-ci.org/tomi77/pyems.svg?branch=master
   :target: https://travis-ci.org/tomi77/pyems
.. image:: https://coveralls.io/repos/github/tomi77/pyems/badge.svg?branch=master
   :target: https://coveralls.io/github/tomi77/pyems?branch=master

Installation
============

Install package via ``pip``

.. sourcecode:: sh

   pip install pyems

Documentation
=============

http://tomi77.github.io/pyems/

API Usage
=========

.. sourcecode:: python

   from pyems import Api

   api = Api('http://127.0.0.1:7777')
   print api.list_streams()

Contribute
==========

Clone repo

.. sourcecode:: sh

 git clone git@github.com:tomi77/pyems.git

Create virtualenv

.. sourcecode:: sh

 mkvirtualenv pyems

Install documentation packages

.. sourcecode:: sh

 pip install sphinx sphinx-rtd-theme


