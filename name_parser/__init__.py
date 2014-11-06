import os
import string
import pycrfsuite
import re
from collections import OrderedDict
import warnings
import config

labels = config.LABELS

try :
    TAGGER = pycrfsuite.Tagger()
    path = os.path.split(os.path.abspath(__file__))[0] + '/usaddr.crfsuite'
    TAGGER.open(path)
except IOError :
    warnings.warn("You must train the model (run training/training.py) and create the usaddr.crfsuite file before you can use the parse and tag methods")

def parse(raw_string) :

    tokens = tokenize(raw_string)

    if not tokens :
        return []

    features = tokens2features(tokens)

    tags = TAGGER.tag(features)
    return zip(tokens, tags)

def tag(raw_string) :
    tagged = OrderedDict()
    for token, label in parse(raw_string) :
        tagged.setdefault(label, []).append(token)

    for token in tagged :
        component = ' '.join(tagged[token])
        component = component.strip(" ,;")
        tagged[token] = component

    return tagged


def tokenize(raw_string) :
    re_tokens = re.compile(r"""
    \(*\b[^\s,;#()]+[.,;)]*   # ['ab. cd,ef '] -> ['ab.', 'cd,', 'ef']
    |
    [#&]                # [^'#abc'] -> ['#']
    """,
                           re.VERBOSE | re.UNICODE)

    tokens = re_tokens.findall(raw_string)

    if not tokens :
        return []

    return tokens


def tokenFeatures(token) :

    if token in (u'&', u'#') :
        token_clean = token
    else :
        token_clean = re.sub(r'(^[\W]*)|([^.\w]*$)', u'', token)
    token_abbrev = re.sub(r'[.]', u'', token_clean.lower())
    features = {'nopunc' : token_abbrev,
                'abbrev' : token_clean[-1] == u'.',
                'case' : casing(token_clean),
                'digits' : digits(token_clean),
                'length' : (u'd:' + unicode(len(token_abbrev))
                            if token_abbrev.isdigit()
                            else u'w:' + unicode(len(token_abbrev))),
                'endsinpunc' : (token[-1]
                                if bool(re.match('.+[^.\w]', token))
                                else False),
                'directional' : token_abbrev in DIRECTIONS,
                'has.vowels'  : bool(set(token_abbrev[1:]) & set('aeiou')),
                }

    return features

def tokens2features(tokens):
    
    feature_sequence = [tokenFeatures(tokens[0])]
    previous_features = feature_sequence[-1].copy()

    for token in tokens[1:] :
        token_features = tokenFeatures(token) 
        current_features = token_features.copy()

        feature_sequence[-1]['next'] = current_features
        token_features['previous'] = previous_features
            
        feature_sequence.append(token_features)

        previous_features = current_features

    feature_sequence[0]['rawstring.start'] = True
    feature_sequence[-1]['rawstring.end'] = True

    if len(feature_sequence) > 1 :
        feature_sequence[1]['previous']['rawstring.start'] = True
        feature_sequence[-2]['next']['rawstring.end'] = True

    return feature_sequence

def casing(token) :
    if token.isupper() :
        return 'upper'
    elif token.islower() :
        return 'lower' 
    elif token.istitle() :
        return 'title'
    else :
        return 'other'

def digits(token) :
    if token.isdigit() :
        return 'all_digits' 
    elif set(token) & set(string.digits) :
        return 'some_digits' 
    else :
        return 'no_digits'
                                    

