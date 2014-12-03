from parserator.manual_labeling import consoleLabel, naiveConsoleLabel
import name_parser
from lxml import etree
import sys
import os.path
import data_prep_utils
import re


if __name__ == '__main__' :

    import csv
    from argparse import ArgumentParser
    import unidecode
    
    labels = name_parser.config.LABELS
    
    parser = ArgumentParser(description="Label some strings")
    parser.add_argument(dest="infile", 
                        help="input csv", metavar="FILE")
    parser.add_argument(dest="outfile", 
                        help="output csv", metavar="FILE")
    parser.add_argument("-n",
                        help="-n for naive labeling (if there isn't an existing .crfsuite settings file)", action="store_true")
    args = parser.parse_args()

    file_slug = re.sub('(.*/)|(.csv)|(unlabeled_)', '', args.infile)

    # Check to make sure we can write to outfile
    if os.path.isfile(args.outfile):
        with open(args.outfile, 'r+' ) as f:
            try :
                tree = etree.parse(f)
            except :
                raise ValueError("%s does not seem to be a valid xml file"
                                 % args.outfile)

    with open(args.infile, 'rU') as infile :
        reader = csv.reader(infile)

        strings = set([unidecode.unidecode(row[0]) for row in reader])

    p = name_parser.Parser()

    if args.n :
        labeled_list, raw_strings_left = naiveConsoleLabel(strings, labels, p)
    else:
        labeled_list, raw_strings_left = consoleLabel(strings, labels, p) 

    data_prep_utils.appendListToXMLfile(labeled_list, args.outfile)
    data_prep_utils.list2file(raw_strings_left, 'training/data_prep/unlabeled_data/unlabeled_'+file_slug+'.csv')
    
