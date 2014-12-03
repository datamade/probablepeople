import parserator
import os
import re
from metaphone import doublemetaphone


class Parser(parserator.Parser):

    LABELS = [
        'PrefixMarital',
        'PrefixOther',
        'GivenName',
        'FirstInitial',
        'MiddleName',
        'MiddleInitial',
        'Surname',
        'LastInitial',
        'SuffixGenerational',
        'SuffixOther',
        'Nickname',
        'And'
        ]
    NULL_LABEL = 'Null'
    PARENT_LABEL = 'Name'
    GROUP_LABEL = 'NameCollection'
    MODEL_FILE = 'learned_settings.crfsuite'
    MODEL_PATH = os.path.split(os.path.abspath(__file__))[0] + '/' + MODEL_FILE
    TRAINING_FILE = 'labeled.xml'
    VOWELS_Y = tuple('aeiouy')

    def tokenize(self, raw_string) :

        re_tokens = re.compile(r"""
        \(*[^\s,;()]+[.,;)]*   # ['ab. cd,ef '] -> ['ab.', 'cd,', 'ef']
        """,
                               re.VERBOSE | re.UNICODE)

        tokens = re_tokens.findall(raw_string)

        if not tokens :
            return []

        return tokens

    def tokens2features(self, tokens):
        
        feature_sequence = [self.tokenFeatures(tokens[0])]
        previous_features = feature_sequence[-1].copy()

        seen_comma = False

        for token in tokens[1:] :
            token_features = self.tokenFeatures(token) 
            if not seen_comma and previous_features['comma'] :
                seen_comma = True
            if seen_comma :
                token_features['seen.comma'] = True

            current_features = token_features.copy()

            feature_sequence[-1]['next'] = current_features
            token_features['previous'] = previous_features        
                
            feature_sequence.append(token_features)

            previous_features = current_features

        if len(feature_sequence) > 1 :
            feature_sequence[0]['rawstring.start'] = True
            feature_sequence[-1]['rawstring.end'] = True
            feature_sequence[1]['previous']['rawstring.start'] = True
            feature_sequence[-2]['next']['rawstring.end'] = True

        else : 
            feature_sequence[0]['singleton'] = True

        return feature_sequence

    def tokenFeatures(self, token) :

        if token in (u'&') :
            token_clean = token_abbrev = token
            
        else :
            token_clean = re.sub(r'(^[\W]*)|([^.\w]*$)', u'', token)
            token_abbrev = re.sub(r'\W', u'', token_clean.lower())

        metaphone = doublemetaphone(token_abbrev)

        features = {'nopunc' : token_abbrev,
                    'abbrev' : token_clean.endswith('.'),
                    'comma'  : token.endswith(','), 
                    'hyphenated' : '-' in token_clean,
                    'contracted' : "'" in token_clean,
                    'bracketed' : bool(re.match(r'["(\']\w+[")\']', token)),
                    'case' : self.casing(token_clean),
                    'length' : len(token_abbrev),
                    'initial' : len(token_abbrev) == 1 and token_abbrev.isalpha(),
                    'has.vowels'  : bool(set(token_abbrev[1:]) & set(self.VOWELS_Y)),
                    'roman' : set('xvi').issuperset(token_abbrev),
                    'endswith.vowel' : token_abbrev.endswith(self.VOWELS_Y),
                    'metaphone1' : metaphone[0],
                    'metaphone2' : (metaphone[1] if metaphone[1] else metaphone[0]),
                    'more.vowels' : self.vowelRatio(token_abbrev)
                    }

        reversed_token = token_abbrev[::-1]
        for i in range(1, len(token_abbrev)) :
            features['prefix_%s' % i] = token_abbrev[:i]
            features['suffix_%s' % i] = reversed_token[:i][::-1]
            if i > 4 :
                break

        return features

    def casing(self, token) :
        if token.isupper() :
            return 'upper'
        elif token.islower() :
            return 'lower' 
        elif token.istitle() :
            return 'title'
        elif token.isalpha() :
            return 'mixed'
        else :
            return False

    def vowelRatio(self, token) :
        n_chars = len(token)
        if n_chars > 1:
            n_vowels = sum(token.count(c) for c in self.VOWELS_Y)
            return n_vowels/float(n_chars)
        else :
            return False


