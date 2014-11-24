import os
import pycrfsuite
import re
from collections import OrderedDict
import warnings
import config

try :
    TAGGER = pycrfsuite.Tagger()
    path = os.path.split(os.path.abspath(__file__))[0] + '/learned_settings.crfsuite'
    TAGGER.open(path)
except IOError :
    warnings.warn("You must train the model (run training/training.py) and create the learned_settings.crfsuite file before you can use the parse and tag methods")

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
    \(*[^\s,;()]+[.,;)]*   # ['ab. cd,ef '] -> ['ab.', 'cd,', 'ef']
    """,
                           re.VERBOSE | re.UNICODE)

    tokens = re_tokens.findall(raw_string)

    if not tokens :
        return []

    return tokens

def tokens2features(tokens):
    
    feature_sequence = [config.tokenFeatures(tokens[0])]
    previous_features = feature_sequence[-1].copy()

    seen_comma = False

    for token in tokens[1:] :
        token_features = config.tokenFeatures(token) 
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
