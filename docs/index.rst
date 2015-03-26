.. probablepeople documentation master file, created by
   sphinx-quickstart on Mon Mar 16 21:43:12 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================
probablepeople |release|
================

probablepeople is a python library for parsing unstructured romanized name or company strings into name components, using advanced NLP methods.

.. toctree::
   :maxdepth: 2


Installation
============

.. code-block:: bash

   pip install probablepeople


Usage
============
The ``parse`` method will split your string into components, and label each component.
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
      >>> probablepeople.parse('Sitwell Housing Inc')
      [('Sitwell', 'CorporationName'),
      ('Housing', 'CorporationName'),
      ('Inc', 'CorporationLegalType')]

The ``tag`` method will return an OrderedDict with distinct labels as keys & parts of your string as values, as well as a string type (``Person``, ``Household``, or ``Corporation``)
   .. code:: python

      >>> import probablepeople
      >>> probablepeople.tag('Mr George "Gob" Bluth II')
      (OrderedDict([
      ('PrefixMarital', 'Mr'), 
      ('GivenName', 'George'), 
      ('Nickname', '"Gob"'), 
      ('Surname', 'Bluth'), 
      ('SuffixGenerational', 'II')]), 
      'Person')
      >>> probablepeople.tag('Lucille & George Bluth')
      (OrderedDict([
      ('GivenName', 'Lucille'), 
      ('And', '&'), 
      ('SecondGivenName', 'George'), 
      ('Surname', 'Bluth')]), 
      'Household')
      >>> probablepeople.tag('Sitwell Housing Inc')
      (OrderedDict([
      ('CorporationName', 'Sitwell Housing'), 
      ('CorporationLegalType', 'Inc')]), 
      'Corporation')


Details
=======

probablepeople has the following labels for parsing names & companies:

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
* CorporationName
* CorporationNameOrganization
* CorporationLegalType
* CorporationNamePossessiveOf
* ShortForm
* ProxyFor
* AKA


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
