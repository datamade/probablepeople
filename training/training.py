import pycrfsuite
import name_parser
import random
import os
from lxml import etree
from imp import reload

NULL_TAG = 'Null'

def trainModel(training_data, model_file,
               params_to_set={'c1':0.1, 'c2':0.01, 'feature.minfreq':0}):

    X = []
    Y = []

    for string_concat, components in training_data:
        tokens, labels = zip(*components)
        X.append(name_parser.tokens2features(tokens))
        Y.append(labels)

    # train model
    trainer = pycrfsuite.Trainer(verbose=False, params=params_to_set)
    for xseq, yseq in zip(X, Y):
        trainer.append(xseq, yseq)

    trainer.train(model_file)
    reload(name_parser)

def parseTrainingData(filepath):
    tree = etree.parse(filepath)
    collection_XML = tree.getroot()

    for sequence_xml in collection_XML:
        components = []
        string_concat = etree.tostring(sequence_xml, method='text')
        string_concat = string_concat.replace('&#38;', '&')
        for component in list(sequence_xml):
            components.append([component.text, component.tag])
            if component.tail and component.tail.strip():
                components.append([component.tail.strip(), NULL_TAG])

        yield string_concat, components


def get_data_sklearn_format(path='training/training_data/labeled.xml'):
    """
    Parses the specified data file and returns it in sklearn format.
    :param path:
    :return: tuple of:
                1) list of training addresses, each of which is a string
                2) list of gold standard labels, each of which is a tuple
                of strings, one for each token in the corresponding training
                address
    """
    data = list(parseTrainingData(path))
    random.shuffle(data)

    x, y = [], []
    for address_text, components in data:
        tokens, labels = zip(*components)
        x.append(address_text)
        y.append(labels)
    return x, y


if __name__ == '__main__':

    root_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

    training_data = list(parseTrainingData(root_path + '/training/training_data/labeled.xml'))

    trainModel(training_data, root_path + '/name_parser/learned_settings.crfsuite')
