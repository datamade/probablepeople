probablepeople
=================
[![Build Status](https://travis-ci.org/datamade/probablepeople.svg?branch=master)](https://travis-ci.org/datamade/probablepeople)

probablepeople is a python library for parsing unstructured romanized name or company strings into components, using advanced NLP methods. This is based off [usaddress](https://github.com/datamade/usaddress), a python library for parsing addresses.

Try it out on our [web interface](https://parserator.datamade.us/probablepeople)! For those who aren't python developers, we also have an [API](https://parserator.datamade.us/api-docs).

**What this can do:** Using a probabilistic model, it makes (very educated) guesses in identifying name or corporation components, even in tricky cases where rule-based parsers typically break down.

**What this cannot do:** It cannot identify components with perfect accuracy, nor can it verify that a given name/company is correct/valid.

probablepeople learns how to parse names/companies through a body of training data. If you have examples of names/companies that stump this parser, please send them over! By adding more examples to the training data, probablepeople can continue to learn and improve.

## How to use the probablepeople python library
1. Install probablepeople with [pip](https://pip.readthedocs.io/en/latest/quickstart.html), a tool for installing and managing python packages ([beginner's guide here](http://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/))

   In the terminal,
   
    ```
    pip install probablepeople  
    ```  
2. Parse some names/companies!
   
   ![pp](https://cloud.githubusercontent.com/assets/1406537/7870535/966f0956-054f-11e5-8312-4d392f79ff75.gif)
    
   Note that `parse` and `tag` are differet methods:
   ```python
   import probablepeople as pp
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

## Links:
* Documentation: https://probablepeople.readthedocs.io/
* Web Interface: http://parserator.datamade.us/probablepeople
* Distribution: https://pypi.python.org/pypi/probablepeople
* Repository: https://github.com/datamade/probablepeople
* Issues: https://github.com/datamade/usaddress/issues
* Blog post: https://datamade.us/blog/parse-name-or-parse-anything-really

## For the nerds:
Probablepeople uses [parserator](https://github.com/datamade/parserator), a library for making and improving probabilistic parsers - specifically, parsers that use [python-crfsuite](https://github.com/tpeng/python-crfsuite)'s implementation of conditional random fields. Parserator allows you to train probablepeople's model (a .crfsuite settings file) on labeled training data, and provides tools for easily adding new labeled training data.
#### Building & testing development code
  
  ```
  git clone https://github.com/datamade/probablepeople.git  
  cd probablepeople  
  pip install -r requirements.txt  
  python setup.py develop
  make all
  nosetests .  
  ```  
#### Creating/adding labeled training data (.xml outfile) from unlabeled raw data (.csv infile)  

If there are name/company formats that the parser isn't performing well on, you can add them to training data. As probablepeople continually learns about new cases, it will continually become smarter and more robust.

*NOTE: The model doesn't need many examples to learn about new patterns - if you are trying to get probablepeople to perform better on a specific type of name, start with a few (<5) examples, check performance, and then add more examples as necessary.*

For this parser, we are keeping person names and organization names separate in the training data. The two training files used to produce the model are:
- `name_data/labeled/labeled.xml` for people
- `name_data/labeled/company_labeled.xml` for organizations.

To add your own training examples, first put your unlabeled raw data in a csv. Then:
  
```
parserator label [infile] [outfile] probablepeople  
```  

`[infile]` is your raw csv and `[outfile]` is the appropriate training file to write to. For example, if you put raw strings in `my_companies.csv`, you'd use `parserator label my_companies.csv name_data/labeled/company_labeled.xml probablepeople`

The parserator `label` command will start a console labeling task, where you will be prompted to label raw strings via the command line. For more info on using parserator, see the [parserator documentation](https://github.com/datamade/parserator/blob/master/README.md).  

#### Re-training the model  
  If you've added new training data, you will need to re-train the model. To set multiple files as traindata, separate them with commas.
  
  ```
  parserator train [traindata] probablepeople  
  ```  
  
  probablepeople allows for multiple model files - `person` for person names only, `company` for company names only, or `generic` (both). here are examples of commands for training models:
  
  ```
  parserator train name_data/labeled/person_labeled.xml,name_data/labeled/company_labeled.xml probablepeople --modelfile=generic
  parserator train name_data/labeled/person_labeled.xml probablepeople --modelfile=person
  parserator train name_data/labeled/company_labeled.xml probablepeople --modelfile=company
  ```  
  
## Errors and Bugs

If something is not behaving intuitively, it is a bug and should be reported.
Report it here by creating an issue: https://github.com/datamade/probablepeople/issues

Help us fix the problem as quickly as possible by following [Mozilla's guidelines for reporting bugs.](https://developer.mozilla.org/en-US/docs/Mozilla/QA/Bug_writing_guidelines#General_Outline_of_a_Bug_Report)

## Patches and Pull Requests

Your patches are welcome. Here's our suggested workflow:

* Fork the project.
* Add your labeled examples.
* Send us a pull request with a description of your work.

### Copyright

Copyright (c) 2014 Atlanta Journal Constitution. Released under the [MIT License](https://github.com/datamade/probablepeople/blob/master/LICENSE).
