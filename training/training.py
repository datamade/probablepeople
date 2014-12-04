import pycrfsuite
import name_parser
import random
import os
from lxml import etree
from imp import reload
import parserator


if __name__ == '__main__':

    p = name_parser.Parser()

    parserator.training.train(p)
    
    reload(name_parser)
