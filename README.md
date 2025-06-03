probabledoctor
=================
[![Build Status](https://travis-ci.org/datamade/probabledoctor.svg?branch=master)](https://travis-ci.org/datamade/probabledoctor)

probabledoctor is a python library for parsing unstructured romanized name or company strings into components, using advanced NLP methods. This is based off [usaddress](https://github.com/datamade/usaddress), a python library for parsing addresses.



**What this can do:** Using a probabilistic model, it makes (very educated) guesses in identifying name or corporation components, even in tricky cases where rule-based parsers typically break down.

**What this cannot do:** It cannot identify components with perfect accuracy, nor can it verify that a given name/company is correct/valid.

probabledoctor learns how to parse names/companies through a body of training data. If you have examples of names/companies that stump this parser, please send them over! By adding more examples to the training data, probabledoctor can continue to learn and improve.

## How to use the probabledoctor python library
1. Install probabledoctor with [pip](https://pip.readthedocs.io/en/latest/quickstart.html), a tool for installing and managing python packages ([beginner's guide here](http://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/))

   In the terminal,
   
    ```
    pip install probabledoctor  
    ```  
2. Parse some names/companies!
   
   ![pp](https://cloud.githubusercontent.com/assets/1406537/7870535/966f0956-054f-11e5-8312-4d392f79ff75.gif)
    
   Note that `parse` and `tag` are differet methods:
   ```python
   import probabledoctor as pp
   name_str='Mr George "Gob" Bluth II'
   corp_str='Sitwell Housing Inc'
  
   # The parse method will split your string into components, and label each component.
   pp.parse(name_str) # expected output: [('Mr', 'PrefixMarital'), ('George', 'GivenName'), ('"Gob"', 'Nickname'), ('Bluth', 'Surname'), ('II', 'SuffixGenerational')]
   pp.parse(corp_str) # expected output: [('Sitwell', 'CorporationName'), ('Housing', 'CorporationName'), ('Inc', 'CorporationLegalType')]
  
   # The tag method will try to be a little smarter
   # it will merge consecutive components, strip commas, & return a string type
   pp.tag(name_str) # expected output: (OrderedDict([('PrefixMarital', 'Mr'), ('GivenName', 'George'), ('Nickname', '"Gob"'), ('Surname', 'Bluth'), ('SuffixGenerational', 'II')]), 'Person')
   pp.tag(corp_str) # expected output: (OrderedDict([('CorporationName', 'Sitwell Housing'), ('CorporationLegalType', 'Inc')]), 'Corporation')
   ```
  
  # Medical professional names
  You can also parse medical professional names, including doctor titles and degree suffixes. For example:
  ```python
  import probabledoctor as pp
  # Parsing with title and medical degree suffix
  >>> pp.parse('Dr. John A. Smith, MD')
  [('Dr.', 'PrefixOther'), ('John', 'GivenName'), ('A.', 'MiddleInitial'), ('Smith', 'Surname'), ('MD', 'SuffixOther')]
  >>> pp.tag('Dr. John A. Smith, MD')
  (OrderedDict([
    ('PrefixOther', 'Dr.'),
    ('GivenName', 'John'),
    ('MiddleInitial', 'A.'),
    ('Surname', 'Smith'),
    ('SuffixOther', 'MD')
  ]), 'Person')
  ```
  
  If you notice titles or degrees not parsed as expected, add some labeled examples and retrain:
  ```bash
  # Label new person examples (e.g., medical professionals)
  parserator label my_medical_names.csv name_data/labeled/person_labeled.xml probabledoctor
  # Retrain the person model to include them
  parserator train name_data/labeled/person_labeled.xml probabledoctor --modelfile=person
  ```

## Links:
* Documentation: https://probabledoctor.readthedocs.io/
* Distribution: https://pypi.python.org/pypi/probabledoctor
* Repository: https://github.com/atk81-candor/probabledoctor#
* Issues: https://github.com/datamade/usaddress/issues
* Blog post: https://datamade.us/blog/parse-name-or-parse-anything-really

## For the nerds:
probabledoctor uses [parserator](https://github.com/datamade/parserator), a library for making and improving probabilistic parsers - specifically, parsers that use [python-crfsuite](https://github.com/tpeng/python-crfsuite)'s implementation of conditional random fields. Parserator allows you to train probabledoctor's model (a .crfsuite settings file) on labeled training data, and provides tools for easily adding new labeled training data.
#### Building & testing development code
  
```console
git clone https://github.com/datamade/probabledoctor.git
cd probabledoctor
pip install -e .
pytest
```

#### Creating/adding labeled training data (.xml outfile) from unlabeled raw data (.csv infile)  

If there are name/company formats that the parser isn't performing well on, you can add them to training data. As probabledoctor continually learns about new cases, it will continually become smarter and more robust.

*NOTE: The model doesn't need many examples to learn about new patterns - if you are trying to get probabledoctor to perform better on a specific type of name, start with a few (<5) examples, check performance, and then add more examples as necessary.*

For this parser, we are keeping person names and organization names separate in the training data. The two training files used to produce the model are:
- `name_data/labeled/labeled.xml` for people
- `name_data/labeled/company_labeled.xml` for organizations.

To add your own training examples, first put your unlabeled raw data in a csv. Then:
  
```
parserator label [infile] [outfile] probabledoctor  
```  

`[infile]` is your raw csv and `[outfile]` is the appropriate training file to write to. For example, if you put raw strings in `my_companies.csv`, you'd use `parserator label my_companies.csv name_data/labeled/company_labeled.xml probabledoctor`

The parserator `label` command will start a console labeling task, where you will be prompted to label raw strings via the command line. For more info on using parserator, see the [parserator documentation](https://github.com/datamade/parserator/blob/master/README.md).  

#### Re-training the model  
  If you've added new training data, you will need to re-train the model. To set multiple files as traindata, separate them with commas.
  
  ```
  parserator train [traindata] probabledoctor  
  ```  
  
  probabledoctor allows for multiple model files - `person` for person names only, `company` for company names only, or `generic` (both). here are examples of commands for training models:
  
  ```
  parserator train name_data/labeled/person_labeled.xml,name_data/labeled/company_labeled.xml probabledoctor --modelfile=generic
  parserator train name_data/labeled/person_labeled.xml probabledoctor --modelfile=person
  parserator train name_data/labeled/company_labeled.xml probabledoctor --modelfile=company
  ```
  
## Errors and Bugs

If something is not behaving intuitively, it is a bug and should be reported.
Report it here by creating an issue: https://github.com/datamade/probabledoctor/issues

Help us fix the problem as quickly as possible by following [Mozilla's guidelines for reporting bugs.](https://developer.mozilla.org/en-US/docs/Mozilla/QA/Bug_writing_guidelines#General_Outline_of_a_Bug_Report)

## Patches and Pull Requests

Your patches are welcome. Here's our suggested workflow:

* Fork the project.
* Add your labeled examples.
* Send us a pull request with a description of your work.

### Copyright

Copyright (c) 2014 Atlanta Journal Constitution. Released under the [MIT License](https://github.com/datamade/probabledoctor/blob/master/LICENSE).
