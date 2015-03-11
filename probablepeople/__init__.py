#!/usr/bin/python
# -*- coding: utf-8 -*-x

from __future__ import division
from builtins import zip
from builtins import range
from past.utils import old_div
import os
import re
from collections import OrderedDict
from metaphone import doublemetaphone
import pycrfsuite
import warnings


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

PARENT_LABEL = 'Name'
GROUP_LABEL = 'NameCollection'

MODEL_FILE = 'learned_settings.crfsuite'

VOWELS_Y = tuple('aeiouy')

try :
    TAGGER = pycrfsuite.Tagger()
    TAGGER.open(os.path.split(os.path.abspath(__file__))[0]+'/'+MODEL_FILE)
except IOError :
    TAGGER = None
    warnings.warn('You must train the model (parserator train [traindata] [modulename]) to create the %s file before you can use the parse and tag methods' %MODEL_FILE)

def parse(raw_string):
    if not TAGGER:
        raise IOError('\nMISSING MODEL FILE: %s\nYou must train the model before you can use the parse and tag methods\nTo train the model annd create the model file, run:\nparserator train [traindata] [modulename]' %MODEL_FILE)

    tokens = tokenize(raw_string)
    if not tokens :
        return []

    features = tokens2features(tokens)

    tags = TAGGER.tag(features)
    return list(zip(tokens, tags))

def tag(raw_string) :
    tagged = OrderedDict()

    prev_label = None
    and_label = False

    for token, label in parse(raw_string) :

        if label == 'And':
            and_label = True
        if and_label and label in tagged:
            label = 'Second'+label

        if label not in tagged:
            tagged[label] = [token]
        elif label == prev_label:
            tagged[label].append(token)
        else:
            print('ORIGINAL STRING: ', raw_string)
            print(parse(raw_string))
            raise ValueError("More than one area of the name has the same label - this may not be a valid parsing")

        prev_label = label

    for token in tagged :
        component = ' '.join(tagged[token])
        component = component.strip(' ,;')
        tagged[token] = component

    return tagged

def tokenize(raw_string) :

    re_tokens = re.compile(r"""
    \(*[^\s,;()]+[.,;)]*   # ['ab. cd,ef '] -> ['ab.', 'cd,', 'ef']
    """,
                           re.VERBOSE | re.UNICODE)

    tokens = re_tokens.findall(raw_string)

    if not tokens :
        return []

    return tokens

def tokens2features(tokens):
    
    feature_sequence = [tokenFeatures(tokens[0])]
    previous_features = feature_sequence[-1].copy()

    seen_comma = False

    for token in tokens[1:] :
        token_features = tokenFeatures(token) 
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

def tokenFeatures(token) :

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
                'case' : casing(token_clean),
                'length' : len(token_abbrev),
                'initial' : len(token_abbrev) == 1 and token_abbrev.isalpha(),
                'has.vowels'  : bool(set(token_abbrev[1:]) & set(VOWELS_Y)),
                'roman' : set('xvi').issuperset(token_abbrev),
                'endswith.vowel' : token_abbrev.endswith(VOWELS_Y),
                'metaphone1' : metaphone[0],
                'metaphone2' : (metaphone[1] if metaphone[1] else metaphone[0]),
                'more.vowels' : vowelRatio(token_abbrev)
                }

    reversed_token = token_abbrev[::-1]
    for i in range(1, len(token_abbrev)) :
        features['prefix_%s' % i] = token_abbrev[:i]
        features['suffix_%s' % i] = reversed_token[:i][::-1]
        if i > 4 :
            break

    return features

def casing(token) :
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

def vowelRatio(token) :
    n_chars = len(token)
    if n_chars > 1:
        n_vowels = sum(token.count(c) for c in VOWELS_Y)
        return old_div(n_vowels,float(n_chars))
    else :
        return False


