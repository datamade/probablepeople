from parserator.manual_labeling import getArgumentParser, label
import name_parser
from lxml import etree
import sys
import os.path
import data_prep_utils
import re


if __name__ == '__main__' :

    arg_parser = getArgumentParser()
    args = arg_parser.parse_args()
    p = name_parser.Parser()

    label(p, args, 'training/data_prep/unlabeled_data/')