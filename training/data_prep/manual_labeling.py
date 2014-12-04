from parserator.manual_labeling import label
import name_parser

if __name__ == '__main__' :

    p = name_parser.Parser()

    label(p, 'training/data_prep/unlabeled_data/')
