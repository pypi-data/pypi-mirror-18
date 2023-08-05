headjack 
=========================

*A python package and command-line tools to download, organize, share, archive and reference various kinds of media. Books, podcasts, articles, videos ...*.

Here's a summary of what's included in the python package:

.. include:: /classes_and_functions.rst


Command-Line Usage
==================

.. code-block:: bash 
   
    
    Documentation for headjack can be found here: http://headjack.readthedocs.org/en/stable
    
    Usage:
        headjack read sendToKindle [-s <pathToSettingsFile>]
        headjack read convert kindleAnnotations [-s <pathToSettingsFile>]
        headjack media (stage|archive) [-s <pathToSettingsFile>]
    
        -h, --help            show this help message
        -s, --settings        the settings file
    

Installation
============

The easiest way to install headjack us to use ``pip``:

.. code:: bash

    pip install headjack

Or you can clone the `github repo <https://github.com/thespacedoctor/headjack>`__ and install from a local version of the code:

.. code:: bash

    git clone git@github.com:thespacedoctor/headjack.git
    cd headjack
    python setup.py install

To upgrade to the latest version of headjack use the command:

.. code:: bash

    pip install headjack --upgrade


Documentation
=============

Documentation for headjack is hosted by `Read the Docs <http://headjack.readthedocs.org/en/stable/>`__ (last `stable version <http://headjack.readthedocs.org/en/stable/>`__ and `latest version <http://headjack.readthedocs.org/en/latest/>`__).

Command-Line Tutorial
=====================

.. todo::

    - add tutorial


To convert a directory of kindle annotation notebook exports:

```bash
headjack read convert kindleAnnotations
```

