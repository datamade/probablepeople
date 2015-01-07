name-parser
=================
name-parser is a python library for parsing unstructured name strings into name components, using advanced NLP methods. This is based off [usaddress](https://github.com/datamade/usaddress), a python library for parsing addresses.

## How to use name-parser
1. Install name-parser
   
    ```
    pip install name_parser  
    ```  
2. Parse some names!
   
    ```
    >>> import name_parser  
    >>> name_parser.parse('Mr George "Gob" Bluth II')  
[('Mr', 'PrefixMarital'), ('George', 'GivenName'), ('"Gob"', 'Nickname'), ('Bluth', 'Surname'), ('II', 'SuffixGenerational')]
    ```  

## For the nerds:
Name parser uses parserator, a library for making and improving probabilistic parsers - specifically, parsers that use [python-crfsuite](https://github.com/tpeng/python-crfsuite)'s implementation of conditional random fields. Parserator allows you to train name-parser's model (a .crfsuite settings file) on labeled training data, and provides tools for easily adding new labeled training data.
#### Building & testing development code
  
  ```
  git clone https://github.com/datamade/name-parser.git  
  cd name-parser  
  pip install -r requirements.txt  
  python setup.py develop  
  parserator train name_data/labeled/labeled.xml name_parser  
  nosetests .  
  ```  
#### Creating/adding labeled training data (.xml outfile) from unlabeled raw data (.csv infile)  
  If there are name formats that the parser isn't performing well on, you can add them to training data. As the name-parser continually learns about new cases, it will continually become smarter and more robust.  
  
```
parserator label [infile] [outfile] name_parser  
```  

We have our labeled example in `name_data/labeled/labeled.xml` so, you can use.

```
parserator label [infile] name_data/labeled/labeled.xml name_parser  
```  

  This will start a console labeling task, where you will be prompted to label raw strings via the command line. For more info on using parserator, see the [parserator documentation](https://github.com/datamade/parserator/blob/master/README.md).  
#### Re-training the model  
  If you've added new training data, you will need to re-train the model. 
  
  ```
  parserator train [traindata] name_parser  
  ```  
  
  for example
  
  ```
  parserator train name_data/labeled/labeled.xml name_parser  
  ```  
  
  To set multiple files as traindata, separate them with commas (e.g. ```name_data/labeled/foo.xml,name_data/labeled/bar.xml```)
  
  Contribute back by sending a pull requests with you added labeled examples.


### Copyright

Copyright (c) 2014 Atlanta Journal Constitution. Released under the [MIT License](https://github.com/datamade/name-parser/blob/master/LICENSE).
