from __future__ import print_function
from builtins import zip
import csv
import probablepeople
from parserator import data_prep_utils
from lxml import etree
import random
import pycrfsuite

def getIncorrect(name_list, correct_tag):
    incorrect_list = []
    for name in name_list:
        labeled_sequence = probablepeople.parse(name)
        string, label = labeled_sequence[0]
        if label != correct_tag:
            incorrect_list.append([(string, correct_tag)])
    print(len(incorrect_list), "/", len(name_list), " incorrect, ", int(float(len(incorrect_list))/float(len(name_list))*100), "%")
    return incorrect_list

def makeTaggedData(filename, correct_tag):
    with open(filename, 'rU') as f:
        reader = csv.reader(f)
        tagged_data = set([ (row[0], correct_tag) for row in reader])
    return tagged_data

def addFailedPreds( tagged_list, train_file ):
    print("adding failures")
    i = 0
    added = 0
    for index, tagged_item in enumerate(tagged_list):
        if index % 20 == 0 :
            print()

        if probablepeople.parse(tagged_item[0]) == [tagged_item]:
            print(".", end=' ')

        else :
            data_prep_utils.appendListToXMLfile( [[tagged_item]], train_file)
            print("*", end=' ')
            added += 1
            i += 1
            if added == 10:
                added = 0
                print("\n", "-"*50, "RETRAINING ", index)
                training_data = list(data_prep_utils.parseTrainingData('training/training_data/labeled.xml'))
                trainModel(training_data, 'probablepeople/learned_settings.crfsuite')

    print("\n", "-"*50, "RETRAINING")
    training_data = list(data_prep_utils.parseTrainingData('training/training_data/labeled.xml'))
    trainModel(training_data, 'probablepeople/learned_settings.crfsuite')
    print(i, " cases added to ", train_file)


def trainModel(training_data, model_file,
               params_to_set={'c1':0.1, 'c2':0.01, 'feature.minfreq':0}):

    X = []
    Y = []

    for string_concat, components in training_data:
        tokens, labels = list(zip(*components))
        X.append(probablepeople.tokens2features(tokens))
        Y.append(labels)

    # train model
    trainer = pycrfsuite.Trainer(verbose=False, params=params_to_set)
    for xseq, yseq in zip(X, Y):
        trainer.append(xseq, yseq)

    trainer.train(model_file)
    reload(probablepeople)


if __name__ == '__main__' :
    
    surname_file = 'training_data_prep/unlabeled_data/Top1000_census_surnames.csv'
    female_file = 'training_data_prep/unlabeled_data/top_female_names_census.csv'
    male_file = 'training_data_prep/unlabeled_data/top_male_names_census.csv'

    surname_list = makeTaggedData(surname_file, 'Surname')
    female_list = makeTaggedData(female_file, 'GivenName')
    male_list = makeTaggedData(male_file, 'GivenName')

    shuffled_list = list(surname_list) + list(female_list) + list(male_list)
    random.shuffle(shuffled_list)

    addFailedPreds(shuffled_list, 'training/training_data/labeled.xml')
    
