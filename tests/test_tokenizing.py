from probablepeople import tokenize
import unittest

class TestTokenizing(unittest.TestCase) :

    def test_split_on_punc(self) :

        assert tokenize('belcher,bob') == ['belcher,', 'bob']
        assert tokenize('bob foo-bar') == ['bob', 'foo-bar']
        assert tokenize('bob foo- bar') == ['bob', 'foo', '-', 'bar']
    
    def test_spaces(self) :

        assert tokenize('foo bar') == ['foo', 'bar']
        assert tokenize('foo  bar') == ['foo', 'bar']
        assert tokenize('foo bar ') == ['foo', 'bar']
        assert tokenize(' foo bar') == ['foo', 'bar']

    def test_capture_punc(self) :

        assert tokenize('bob b.') == ['bob', 'b.']
        assert tokenize('bob b., jr') == ['bob', 'b.,', 'jr' ]
        assert tokenize('bob b. jr') == ['bob', 'b.', 'jr' ]
        assert tokenize("robert 'bob' belcher") == ['robert', "'bob'", 'belcher']
        assert tokenize('robert "bob" belcher') == ['robert', '"bob"', 'belcher']

    def test_ampersand(self) :
        assert tokenize('mr & mrs') == ['mr', '&', 'mrs']

    def test_care_of(self) :
        assert tokenize('same c/o me') == ['same', 'c/o', 'me']

    def test_slash(self) :
        assert tokenize('same o/c me') == ['same', 'o', '/', 'c', 'me']

    def test_paren(self) :
        assert tokenize('robert (bob) belcher') == ['robert', '(bob)', 'belcher']
        assert tokenize('robert(bob) belcher') == ['robert', '(bob)', 'belcher']
        assert tokenize('robert (bob)belcher') == ['robert', '(bob)', 'belcher'] 

if __name__ == '__main__' :
    unittest.main()    
