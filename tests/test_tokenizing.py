import name_parser
import unittest

p = name_parser.Parser()

class TestTokenizing(unittest.TestCase) :

    def test_split_on_punc(self) :

        assert p.tokenize('belcher,bob') == ['belcher,', 'bob']
        assert p.tokenize('bob foo-bar') == ['bob', 'foo-bar']
    
    def test_spaces(self) :

        assert p.tokenize('foo bar') == ['foo', 'bar']
        assert p.tokenize('foo  bar') == ['foo', 'bar']
        assert p.tokenize('foo bar ') == ['foo', 'bar']
        assert p.tokenize(' foo bar') == ['foo', 'bar']

    def test_capture_punc(self) :

        assert p.tokenize('bob b.') == ['bob', 'b.']
        assert p.tokenize('bob b., jr') == ['bob', 'b.,', 'jr' ]
        assert p.tokenize('bob b. jr') == ['bob', 'b.', 'jr' ]
        assert p.tokenize("robert 'bob' belcher") == ['robert', "'bob'", 'belcher']
        assert p.tokenize('robert "bob" belcher') == ['robert', '"bob"', 'belcher']

    def test_ampersand(self) :
        assert p.tokenize('mr & mrs') == ['mr', '&', 'mrs']

    def test_paren(self) :
        assert p.tokenize('robert (bob) belcher') == ['robert', '(bob)', 'belcher']
        assert p.tokenize('robert(bob) belcher') == ['robert', '(bob)', 'belcher']
        assert p.tokenize('robert (bob)belcher') == ['robert', '(bob)', 'belcher'] 

if __name__ == '__main__' :
    unittest.main()    
