import name_parser
from lxml import etree
import sys
import os.path

####### test this #############
def consoleLabel(raw_strings, labels): 
    print "Start console labeling!"

    valid_responses = ['y', 'n', 's', 'f', '']
    finished = False

    strings_left_to_tag = raw_strings.copy()
    total_strings = len(raw_strings)
    tagged_strings = set([])

    for i, raw_sequence in enumerate(raw_strings, 1):

        if not finished:

            print "(%s of %s)" % (i, total_strings)
            print "-"*50
            print "STRING: ", raw_sequence
            
            preds = name_parser.parse(raw_sequence)

            user_input = None 
            while user_input not in valid_responses :

                friendly_repr = [(token[0], token[1]) for token in preds]
                print_table(friendly_repr)

                sys.stderr.write('Is this correct? (y)es / (n)o / (s)kip / (f)inish tagging\n')
                user_input = sys.stdin.readline().strip()

                if user_input =='y':
                    tagged_strings.add(tuple(preds))
                    strings_left_to_tag.remove(raw_sequence)

                elif user_input =='n':
                    corrected_string = manualTagging(preds, 
                                                labels)
                    tagged_strings.add(tuple(corrected_string))
                    strings_left_to_tag.remove(raw_sequence)


                elif user_input in ('' or 's') :
                    print "Skipped\n"
                elif user_input == 'f':
                    finished = True

    print "Done! Yay!"
    return tagged_strings, strings_left_to_tag


def print_table(table):
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table:
        print "| %s |" % " | ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line))
        

####### test this #############
def manualTagging(preds, labels):
    valid_input_tags = dict( (str(i), label) for i, label in enumerate(labels))
    tagged_sequence = []
    for token_pred in preds:
        valid_tag = False
        while not valid_tag:
            print 'What is \''+token_pred[0]+'\' ? If '+ token_pred[1] +' hit return' #where should the tag list be printed?
            user_input_tag = sys.stdin.readline().strip()
            if user_input_tag in valid_input_tags or user_input_tag == '':
                valid_tag = True
            else:
                print 'These are the valid inputs:'
                for i in range(len(label_options)):
                    print i, ": ", valid_input_tags[str(i)]

        xml_tag = ''
        if user_input_tag == '':
            xml_tag = token_pred[1]
        else:
            xml_tag = labels[int(user_input_tag)]

        tagged_sequence.append((token[0], xml_tag))
    return tagged_sequence


def appendListToXML(list_to_append, collection_XML) :
    for labeled_sequence in list_to_append:
        sequence_xml = sequence2XML(labeled_sequence)
        collection_XML.append(sequence_xml)
    return collection_XML

def sequence2XML(labeled_sequence) :
    parent_tag = name_parser.config.PARENT_LABEL
    sequence_xml = etree.Element(parent_tag)
    for token, label in labeled_sequence:
        component_xml = etree.Element(label)
        component_xml.text = token
        component_xml.tail = ' '
        sequence_xml.append(component_xml)
    sequence_xml[-1].tail = ''
    return sequence_xml


def stripFormatting(collection) :
    collection.text = None 
    for element in collection :
        element.text = None
        element.tail = None
        
    return collection


def appendListToXMLfile(labeled_list, filepath):

    if os.path.isfile(filepath):
        with open( filepath, 'r+' ) as f:
            tree = etree.parse(filepath)
            collection_XML = tree.getroot()
            collection_XML = stripFormatting(collection_XML)

    else:
        collection_tag = name_parser.config.GROUP_LABEL
        collection_XML = etree.Element(collection_tag)


    collection_XML = appendListToXML(labeled_list, collection_XML)


    with open(filepath, 'w') as f :
        f.write(etree.tostring(collection_XML, pretty_print = True)) 


############# better way to write to csv?
def list2file(string_list, filepath):
    file = open( filepath, 'w' )
    for string in string_list:
        file.write('"%s"\n' % string)


def naiveConsoleLabel(raw_strings, labels): 
    print "Start console labeling!"

    valid_responses = ['t', 's', 'f', '']
    finished = False

    strings_left_to_tag = raw_strings.copy()
    total_strings = len(raw_strings)
    tagged_strings = set([])

    for i, raw_sequence in enumerate(raw_strings, 1):
        if not finished:

            print "(%s of %s)" % (i, total_strings)
            print "-"*50
            print "STRING: ", raw_sequence
            
            tokens = name_parser.tokenize(raw_sequence)

            user_input = None 
            while user_input not in valid_responses :

                sys.stderr.write('(t)ag / (s)kip / (f)inish tagging\n')
                user_input = sys.stdin.readline().strip()

                if user_input =='t' or user_input == '':
                    tagged_sequence = naiveManualTag(tokens, labels)
                    tagged_strings.add(tuple(tagged_sequence))
                    strings_left_to_tag.remove(raw_sequence)

                elif user_input == 's':
                    print "Skipped\n"
                elif user_input == 'f':
                    finished = True

    print "Done! Yay!"
    return tagged_strings, strings_left_to_tag

def naiveManualTag(raw_sequence, labels):
    valid_input_tags = dict((str(i), label) for i, label in enumerate(labels))
    sequence_labels = []
    for token in raw_sequence:
        valid_tag = False
        while not valid_tag:
            print 'What is \''+token+'\' ?'
            user_input_tag = sys.stdin.readline().strip()
            if user_input_tag in valid_input_tags:
                valid_tag = True
            else:
                print "These are the valid inputs:"
                for i in range(len(labels)):
                    print i, ": ", valid_input_tags[str(i)]
        token_label = labels[int(user_input_tag)]
        sequence_labels.append((token, token_label))
    return sequence_labels



if __name__ == '__main__' :

    import csv
    from argparse import ArgumentParser
    import unidecode
    
    labels = name_parser.labels
    
    parser = ArgumentParser(description="Label some strings")
    parser.add_argument(dest="infile", 
                        help="input csv", metavar="FILE")
    parser.add_argument(dest="outfile", 
                        help="output csv", metavar="FILE")
    parser.add_argument("-n",
                        help="-n for naive labeling (if there isn't an existing .crfsuite settings file)", action="store_true")
    args = parser.parse_args()

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

    if args.n :
        labeled_list, raw_strings_left = naiveConsoleLabel(strings, labels)
    else:
        labeled_list, raw_strings_left = consoleLabel(strings, labels) 

    appendListToXMLfile(labeled_list, args.outfile)
    list2file(raw_strings_left, 'training/data_prep/unlabeled_data/unlabeled.csv')
    
