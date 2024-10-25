import pytest
from parserator.training import readTrainingData

from probablepeople import GROUP_LABEL, parse, tag


# these are basic name patterns
def test_basic():
    tagged, name_type = tag("Bob Belcher")
    assert name_type == "Person"
    assert "Bob" == tagged["GivenName"]
    assert "Belcher" == tagged["Surname"]


# for making sure that performance isn't degrading
# from now on, labeled examples of new name formas
# should go in both training data & test data
@pytest.mark.parametrize(
    "name_text,components",
    readTrainingData(["tests/test_data_labeled.xml"], GROUP_LABEL),
)
def test_simple_addresses(name_text, components):

    _, labels_true = list(zip(*components))
    _, labels_pred = list(zip(*parse(name_text)))
    assert labels_pred == labels_true
