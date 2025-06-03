.. probabledoctor documentation master file, created by
   sphinx-quickstart on Mon Mar 16 21:43:12 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================
probabledoctor |release|
================

probabledoctor is a python library for parsing unstructured romanized name or company strings into name components, using advanced NLP methods.

.. toctree::
   :maxdepth: 2


Installation
============

.. code-block:: bash

   pip install probabledoctor


Usage
============
The ``parse`` method will split your string into components, and label each component.
   .. code:: python

      >>> import probabledoctor
      >>> probabledoctor.parse('Mr George "Gob" Bluth II')
      [('Mr', 'PrefixMarital'), 
      ('George', 'GivenName'), 
      ('"Gob"', 'Nickname'), 
      ('Bluth', 'Surname'), 
      ('II', 'SuffixGenerational')]
      >>> probabledoctor.parse('Lucille & George Bluth')
      [('Lucille', 'GivenName'), 
      ('&', 'And'), 
      ('George', 'GivenName'), 
      ('Bluth', 'Surname')]
      >>> probabledoctor.parse('Sitwell Housing Inc')
      [('Sitwell', 'CorporationName'),
      ('Housing', 'CorporationName'),
      ('Inc', 'CorporationLegalType')]

The ``tag`` method will return an OrderedDict with distinct labels as keys & parts of your string as values, as well as a string type (``Person``, ``Household``, or ``Corporation``)
   .. code:: python

      >>> import probabledoctor
      >>> probabledoctor.tag('Mr George "Gob" Bluth II')
      (OrderedDict([
      ('PrefixMarital', 'Mr'), 
      ('GivenName', 'George'), 
      ('Nickname', '"Gob"'), 
      ('Surname', 'Bluth'), 
      ('SuffixGenerational', 'II')]), 
      'Person')
      >>> probabledoctor.tag('Lucille & George Bluth')
      (OrderedDict([
      ('GivenName', 'Lucille'), 
      ('And', '&'), 
      ('SecondGivenName', 'George'), 
      ('Surname', 'Bluth')]), 
      'Household')
      >>> probabledoctor.tag('Sitwell Housing Inc')
      (OrderedDict([
      ('CorporationName', 'Sitwell Housing'), 
      ('CorporationLegalType', 'Inc')]), 
      'Corporation')

Examples: Medical professional names
----------------------------------
You can also parse medical professional names, including doctor titles and degree suffixes:
.. code:: python

   >>> import probabledoctor
   >>> probabledoctor.parse('Dr. John A. Smith, MD')
   [('Dr.', 'PrefixOther'), ('John', 'GivenName'), ('A.', 'MiddleInitial'), ('Smith', 'Surname'), ('MD', 'SuffixOther')]
   >>> probabledoctor.tag('Dr. John A. Smith, MD')
   (OrderedDict([
     ('PrefixOther', 'Dr.'),
     ('GivenName', 'John'),
     ('MiddleInitial', 'A.'),
     ('Surname', 'Smith'),
     ('SuffixOther', 'MD')
   ]), 'Person')

If titles or degrees are not recognized, add labeled examples and retrain:
.. code:: bash

   # Label new person examples (e.g., medical professionals)
   parserator label my_medical_names.csv name_data/labeled/person_labeled.xml probabledoctor
   # Retrain the person model to include them
   parserator train name_data/labeled/person_labeled.xml probabledoctor --modelfile=person

Because the ``tag`` method returns an OrderedDict with labels as keys, it will throw a ``RepeatedLabelError`` error when multiple areas of a name have the same label, and thus can't be concatenated. When ``RepeatedLabelError`` is raised, it is likely that either (1) the input string is not a valid person/corporation name, or (2) some tokens were labeled incorrectly.

``RepeatedLabelError`` has the attributes ``original_string`` (the input string) and ``parsed_string`` (the output of the ``parse`` method on the input string). You can use these attributes to write custom exception handling, for example:
   .. code:: python

       try:
       tagged_name, name_type = probabledoctor.tag(string)
       except probabledoctor.RepeatedLabelError as e :
           some_special_instructions(e.parsed_string, e.original_string)


If you already know that the string refers to a person or a company, you can indicate that to probable people by using the ``type`` argument of the ``parse`` and ``tag`` methods. Valid options are ``'person'`` and ``'company'``.

    .. code:: python
       >>> probabledoctor.tag('Lucille & George Bluth')
       (OrderedDict([
       ('GivenName', 'Lucille'),
       ('And', '&'),
       ('SecondGivenName', 'George'),
       ('Surname', 'Bluth')]),
       'Household')
       >>> probabledoctor.tag('Lucille & George Bluth', type='person')
       (OrderedDict([
       ('GivenName', 'Lucille'),
       ('And', '&'),
       ('SecondGivenName', 'George'),
       ('Surname', 'Bluth')]),
       'Household')
       >>> probabledoctor.tag('Lucille & George Bluth', type='company')
       (OrderedDict([
       ('CorporationName', 'Lucille & George Bluth')]),
       'Corporation')
	   
Details
=======

probabledoctor has the following labels for parsing names & companies:

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

* Documentation: https://probabledoctor.readthedocs.io/



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
