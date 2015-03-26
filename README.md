probablepeople
=================
[![Build Status](https://travis-ci.org/datamade/probablepeople.svg?branch=master)](https://travis-ci.org/datamade/probablepeople)

probablepeople is a python library for parsing unstructured romanized name strings into name components, using advanced NLP methods. This is based off [usaddress](https://github.com/datamade/usaddress), a python library for parsing addresses.

**What this can do:** Using a probabilistic model, it makes (very educated) guesses in identifying name components, even in tricky cases where rule-based parsers typically break down.

**What this cannot do:** It cannot identify name components with perfect accuracy, nor can it verify that a given name is correct/valid.

probablepeople learns how to parse names through a body of training data. If you have a dataset of name strings, or examples of names that stump this parser, please send them over! By adding more examples to the training data, probablepeople can continue to learn and improve.

## How to use probablepeople
1. Install probablepeople
   
    ```
    pip install probablepeople  
    ```  
2. Parse some names!
   
    ```
    >>> import probablepeople  
    >>> probablepeople.parse('Mr George "Gob" Bluth II')  
[('Mr', 'PrefixMarital'), ('George', 'GivenName'), ('"Gob"', 'Nickname'), ('Bluth', 'Surname'), ('II', 'SuffixGenerational')]
    ```  

## Links:
* Documentation: http://probablepeople.rtfd.org/
* Web Interface: http://parserator.datamade.us/probablepeople
* Distribution: https://pypi.python.org/pypi/probablepeople
* Repository: https://github.com/datamade/probablepeople
* Issues: https://github.com/datamade/usaddress/issues
* Blog post: http://datamade.us/blog/parse-name-or-parse-anything-really/

## For the nerds:
Probablepeople uses [parserator](https://github.com/datamade/parserator), a library for making and improving probabilistic parsers - specifically, parsers that use [python-crfsuite](https://github.com/tpeng/python-crfsuite)'s implementation of conditional random fields. Parserator allows you to train probablepeople's model (a .crfsuite settings file) on labeled training data, and provides tools for easily adding new labeled training data.
#### Building & testing development code
  
  ```
  git clone https://github.com/datamade/probablepeople.git  
  cd probablepeople  
  pip install -r requirements.txt  
  python setup.py develop
  parserator train name_data/labeled/labeled.xml,name_data/labeled/company_labeled.xml probablepeople
  nosetests .  
  ```  
#### Creating/adding labeled training data (.xml outfile) from unlabeled raw data (.csv infile)  
  If there are name formats that the parser isn't performing well on, you can add them to training data. As probablepeople continually learns about new cases, it will continually become smarter and more robust.  
  
```
parserator label [infile] [outfile] probablepeople  
```  

We have our labeled example in `name_data/labeled/labeled.xml` so, you can use.

```
parserator label [infile] name_data/labeled/labeled.xml probablepeople  
```  

  This will start a console labeling task, where you will be prompted to label raw strings via the command line. For more info on using parserator, see the [parserator documentation](https://github.com/datamade/parserator/blob/master/README.md).  
#### Re-training the model  
  If you've added new training data, you will need to re-train the model. 
  
  ```
  parserator train [traindata] probablepeople  
  ```  
  
  for example
  
  ```
  parserator train name_data/labeled/labeled.xml probablepeople  
  ```  
  
  To set multiple files as traindata, separate them with commas (e.g. ```name_data/labeled/foo.xml,name_data/labeled/bar.xml```)
  
  Contribute back by sending a pull requests with your added labeled examples.


### Copyright

Copyright (c) 2014 Atlanta Journal Constitution. Released under the [MIT License](https://github.com/datamade/probablepeople/blob/master/LICENSE).
