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
import string
from .ratios import ratios
from .gender import gender_names

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
    'And',
    'CorporationName',
    'CorporationNameOrganization',
    'CorporationNameAndCompany',
    'CorporationNameBranchType',
    'CorporationNameBranchIdentifier',
    'CorporationCommitteeType',
    'CorporationLegalType',
    'ShortForm',
    'ProxyFor',
    'AKA',
    ]

PARENT_LABEL = 'Name'
GROUP_LABEL = 'NameCollection'

MODEL_FILE = 'learned_settings.crfsuite'

VOWELS_Y = tuple('aeiouy')
PREPOSITIONS = {'for', 'to', 'of', 'on'}

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
    proxy_label = False
    aka_label = False

    interrupting_tags = ('CorporationNameOrganization', 
                         'CorporationNameBranchType',
                         'CorporationNameBranchIdentifier',
                         'ProxiedCorporationNameOrganization', 
                         'OtherCorporationNameOrganization',
                         'OtherCorporationNameBranchType',
                         'OtherCorporationNameBranchIdentifier')

    for token, label in parse(raw_string) :
        original_label = label

        if label == 'And':
            and_label = True
        elif label == 'AKA' :
            aka_label = True
        elif label == 'ProxyFor' :
            proxy_label = True

        elif and_label and label in tagged:
            label = 'Second'+label
        elif aka_label and label in tagged :
            label = 'Other'+label
        elif proxy_label and label in tagged :
            label = 'Proxied'+label

        if label not in tagged:
            tagged[label] = [token]

        elif label == prev_label or prev_label in interrupting_tags :
            tagged[label].append(token)
        elif label in interrupting_tags :
            tagged[label].append(token)

        else:
            raise RepeatedLabelError(raw_string, parse(raw_string), label)

        prev_label = label

    for label in tagged :
        component = ' '.join(tagged[label])
        component = component.strip(' ,;')
        tagged[label] = component

    if 'CorporationName' in tagged or 'ShortForm' in tagged :
        name_type = 'Corporation'
    elif and_label :
        name_type = 'Household'
    else :
        name_type = 'Person'

    return tagged, name_type

def tokenize(raw_string) :

    if isinstance(raw_string, bytes):
        try:
            raw_string = str(raw_string, encoding='utf-8')
        except:
            raw_string = str(raw_string)

    re_tokens = re.compile(r"""
    \bc/o\b
    |
    [("']*\b[^\s\/,;#&()]+\b[.,;:'")]* # ['a-b. cd,ef- '] -> ['a-b.', 'cd,', 'ef']
    |
    [#&@/]
    """,
                           re.I | re.VERBOSE | re.UNICODE)

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
        token_clean = re.sub(r'(^[\W]*)|([^.\w]*$)', u'', token.lower())
        token_abbrev = re.sub(r'\W', u'', token_clean)

    metaphone = doublemetaphone(token_abbrev)

    features = {'nopunc' : token_abbrev,
                'abbrev' : token_clean.endswith('.'),
                'comma'  : token.endswith(','), 
                'hyphenated' : '-' in token_clean,
                'contracted' : "'" in token_clean,
                'bracketed' : bool(re.match(r'(["(\']\w+)|(\w+[")\'])', token) and not re.match(r'["(\']\w+[")\']', token)),
                'fullbracketed' : bool(re.match(r'["(\']\w+[")\']', token)),
                'length' : len(token_abbrev),
                'initial' : len(token_abbrev) == 1 and token_abbrev.isalpha(),
                'has.vowels'  : bool(set(token_abbrev[1:]) & set(VOWELS_Y)),
                'just.letters' : token_abbrev.isalpha(),
                'roman' : set('xvi').issuperset(token_abbrev),
                'endswith.vowel' : token_abbrev.endswith(VOWELS_Y),
                'digits' : digits(token_abbrev),
                'metaphone1' : metaphone[0],
                'metaphone2' : (metaphone[1] if metaphone[1] else metaphone[0]),
                'more.vowels' : vowelRatio(token_abbrev),
                'in.names' : token_abbrev.upper() in ratios,
                'prepositions' : token_abbrev in PREPOSITIONS,
                'first.name' : ratios.get(token_abbrev.upper(), 0),
                'gender_ratio' : gender_names.get(token_abbrev, False),
                'possessive' : token_clean.endswith("'s") 
                }

    reversed_token = token_abbrev[::-1]
    for i in range(1, len(token_abbrev)) :
        features['prefix_%s' % i] = token_abbrev[:i]
        features['suffix_%s' % i] = reversed_token[:i][::-1]
        if i > 4 :
            break

    for tri_gram in ngrams(token_abbrev, 3) :
        features[tri_gram] = True

    for four_gram in ngrams(token_abbrev, 4) :
        features[four_gram] = True

    return features

def vowelRatio(token) :
    n_chars = len(token)
    if n_chars > 1:
        n_vowels = sum(token.count(c) for c in VOWELS_Y)
        return old_div(n_vowels,float(n_chars))
    else :
        return False

def digits(token) :
    if token.isdigit() :
        return 'all_digits' 
    elif set(token) & set(string.digits) :
        return 'some_digits' 
    else :
        return 'no_digits'


def ngrams(word, n=2):
    return (''.join(letters) for letters in zip(*[word[i:] for i in range(n)]))

class RepeatedLabelError(Exception) :
    def __init__(self, original_string, parsed_string, repeated_label) :

        message ='''

ERROR: Unable to tag this string because more than one area of the string has the same label

ORIGINAL STRING:  %s
PARSED TOKENS:    %s
UNCERTAIN LABEL:  %s

When this error is raised, it's likely that either (1) the string is not a valid person/corporation name or (2) some tokens were labeled incorrectly

To report an error in labeling a valid name, open an issue at https://github.com/datamade/probablepeople/issues/new - it'll help us continue to improve probablepeople!

For more information, see the documentation at http://probablepeople.readthedocs.org/
        '''%(original_string, parsed_string, repeated_label)

        super(RepeatedLabelError, self).__init__(message)

        self.original_string = original_string
        self.parsed_string = parsed_string

