import csv
import name_parser
import data_prep_utils
from lxml import etree

def getIncorrect(name_list, correct_tag):
    incorrect_list = []
    for name in name_list:
        labeled_sequence = name_parser.parse(name)
        string, label = labeled_sequence[0]
        if label != correct_tag:
            incorrect_list.append([(string, correct_tag)])

    return incorrect_list


if __name__ == '__main__' :

    with open('training/data_prep/unlabeled_data/Top1000_census_surnames.csv', 'rU') as infile:
        reader = csv.reader(infile)
        census_surnames = set([row[0] for row in reader])
    incorrectly_labeled_surnames = getIncorrect(census_surnames, "Surname")

    # limit these to top n surnames?
    data_prep_utils.appendListToXMLfile(incorrectly_labeled_surnames[:200], 'training/training_data/census_surnames.xml')




    with open('training/data_prep/unlabeled_data/top_female_names_census.csv', 'rU') as infile:
        reader = csv.reader(infile)
        census_female = set([row[0] for row in reader])

    with open('training/data_prep/unlabeled_data/top_male_names_census.csv', 'rU') as infile:
        reader = csv.reader(infile)
        census_male = set([row[0] for row in reader])

    incorrectly_labeled_female = getIncorrect(census_female, "GivenName")
    incorrectly_labeled_male = getIncorrect(census_male, "GivenName")

    # limit these to top n names?
    data_prep_utils.appendListToXMLfile(incorrectly_labeled_female[:100], 'training/training_data/census_female.xml')
    data_prep_utils.appendListToXMLfile(incorrectly_labeled_male[:100], 'training/training_data/census_male.xml')

    xml_file_list = [   'training/training_data/census_surnames.xml', 
                        'training/training_data/manually_labeled.xml',
                        'training/training_data/census_female.xml',
                        'training/training_data/census_male.xml'
                        ]

    data_prep_utils.smushXML( xml_file_list, 'training/training_data/labeled.xml')

    