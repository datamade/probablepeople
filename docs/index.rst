.. probablepeople documentation master file, created by
   sphinx-quickstart on Mon Mar 16 21:43:12 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================
probablepeople |release|
================

probablepeople is a python library for parsing unstructured romanized name strings into name components, using advanced NLP methods.

.. toctree::
   :maxdepth: 2


Installation
============

.. code-block:: bash

   pip install probablepeople


Usage
============
The ``parse`` method will split your name string into components, and label each component.
   .. code:: python

      >>> import probablepeople
      >>> probablepeople.parse('Mr George "Gob" Bluth II')  
      [('Mr', 'PrefixMarital'), 
      ('George', 'GivenName'), 
      ('"Gob"', 'Nickname'), 
      ('Bluth', 'Surname'), 
      ('II', 'SuffixGenerational')]
      >>> probablepeople.parse('Lucille & George Bluth')
      [('Lucille', 'GivenName'), 
      ('&', 'And'), 
      ('George', 'GivenName'), 
      ('Bluth', 'Surname')]

The ``tag`` method will return an OrderedDict with distinct name labels as keys & parts of your string as values, as well as a name type (``Person Name`` or ``Couple Names``)
   .. code:: python

      >>> import probablepeople
      >>> probablepeople.tag('Mr George "Gob" Bluth II')
      (OrderedDict([
      ('PrefixMarital', 'Mr'), 
      ('GivenName', 'George'), 
      ('Nickname', '"Gob"'), 
      ('Surname', 'Bluth'), 
      ('SuffixGenerational', 'II')]), 
      'PersonName')
      >>> probablepeople.tag('Lucille & George Bluth')
      (OrderedDict([
      ('GivenName', 'Lucille'), 
      ('And', '&'), 
      ('SecondGivenName', 'George'), 
      ('Surname', 'Bluth')]), 
      'CoupleNames')


Details
=======

probablepeople has the following labels for parsing names:

* PrefixMarital
* PrefixOther
* GivenName
* FirstInitial
* MiddleName
* MiddleInitial
* Surname
* LastInitial
* SuffixGenerational
* SuffixOther
* Nickname
* And


Important links
===============

* Documentation: http://probablepeople.rtfd.org/
* Repository: https://github.com/datamade/probablepeople
* Issues: https://github.com/datamade/probablepeople/issues
* Distribution: https://pypi.python.org/pypi/probablepeople
* Blog Post: http://datamade.us/blog/parse-name-or-parse-anything-really/
* Web Interface: http://parserator.datamade.us/probablepeople



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
