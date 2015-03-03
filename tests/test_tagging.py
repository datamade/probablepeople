from probablepeople import tag
import unittest

class TestTagging(unittest.TestCase) :

    def test_basic(self) :
        tagged = tag("Bob Belcher")
        self.assertEqual("Bob", tagged['GivenName'])
        self.assertEqual("Belcher", tagged['Surname'])
    
