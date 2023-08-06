Kinto Distribution
==================

|travis|

.. |travis| image:: https://travis-ci.org/mozilla-services/kinto-dist.svg?branch=master
    :target: https://travis-ci.org/mozilla-services/kinto-dist


This repository contains:

1. a Pip requirements file that combines all packages needed
   to run a Kinto server will a known good set of deps
2. a configuration file to run it


To install it, make sure you have Python 2.x or 3.x with virtualenv, and run::

    $ make install

To run the server::

    $ make serve

To update kinto-admin::

    $ make update-kinto-admin
