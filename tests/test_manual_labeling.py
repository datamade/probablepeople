import training
from training.data_prep.manual_labeling import sequence2XML
from lxml import etree
import unittest


class TestManualsequence2XML(unittest.TestCase) :

    def test_single_component(self) :

        test_input = [ ('bob', 'foo') ]
        expected_xml = '<Name><foo>bob</foo></Name>'
        assert etree.tostring( sequence2XML(test_input) ) == expected_xml

    def test_two_components(self) :

        test_input = [ ('bob', 'foo'), ('b', 'bar') ]
        expected_xml = '<Name><foo>bob</foo> <bar>b</bar></Name>'
        assert etree.tostring( sequence2XML(test_input) ) == expected_xml

    def test_multiple_components(self) :

        test_input = [ ('bob', 'foo'), ('b', 'bar'), ('sr', 'foobar') ]
        expected_xml = '<Name><foo>bob</foo> <bar>b</bar> <foobar>sr</foobar></Name>'

        assert etree.tostring( sequence2XML(test_input) ) == expected_xml


if __name__ == '__main__' :
    unittest.main()    
