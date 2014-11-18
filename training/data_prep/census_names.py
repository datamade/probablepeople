import csv
import name_parser
import data_prep_utils
from lxml import etree

labels = name_parser.labels

with open('training/data_prep/unlabeled_data/Top1000_census_surnames.csv', 'rU') as infile:
    reader = csv.reader(infile)
    census_surnames = set([row[0] for row in reader])

incorrectly_labeled_surnames = []

for surname in census_surnames:
    labeled_sequence = name_parser.parse(surname)
    string, label = labeled_sequence[0]
    if label != 'Surname':
        incorrectly_labeled_surnames.append([(string, 'Surname')])

# limit these to top n surnames?
data_prep_utils.appendListToXMLfile(incorrectly_labeled_surnames, 'training/training_data/census_surnames.xml')

