from probablepeople import tag, parse, GROUP_LABEL
import unittest
from parserator.training import readTrainingData

class TestTagging(object) :

    # these are basic address patterns
    def test_basic(self) :
        tagged, name_type = tag("Bob Belcher")
        assert name_type == 'Person'
        assert "Bob" == tagged['GivenName']
        assert "Belcher" == tagged['Surname']

    # for making sure that performance isn't degrading
    # from now on, labeled examples of new name formas
    # should go in both training data & test data
    def test_performance(self) :
        test_file = 'tests/test_data_labeled.xml'
        test_data = list(readTrainingData([test_file], GROUP_LABEL))

        for labeled_name in test_data :
            raw_string, components = labeled_name
            _, labels_true = list(zip(*components))
            _, labels_pred = list(zip(*parse(raw_string)))
            yield equals, raw_string, labels_pred, labels_true


def equals(raw_string, 
           labels_pred, 
           labels_true) :
    print("NAME:    ", raw_string)
    print("pred:    ", labels_pred)
    print("true:    ", labels_true)
    assert labels_pred == labels_true


if __name__== "__main__":
    unittest.main()