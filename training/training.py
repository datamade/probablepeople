import pycrfsuite
import name_parser
import random
import os
from lxml import etree
from imp import reload
import parserator


if __name__ == '__main__':

    root_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

    training_data = list(parserator.training.readTrainingData(root_path + '/training/training_data/labeled.xml'))

    p = name_parser.Parser()
    parserator.training.trainModel(training_data, root_path + '/name_parser/learned_settings.crfsuite', p)
    reload(name_parser)
