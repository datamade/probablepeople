#!/usr/bin/python

import os
import re
import string
import typing
import warnings

import probableparsing
import pycrfsuite
from doublemetaphone import doublemetaphone

from .gender import gender_names
from .ratios import ratios

Feature = dict[str, typing.Union[str, bool, "Feature"]]

LABELS = [
    "PrefixMarital",
    "PrefixOther",
    "GivenName",
    "FirstInitial",
    "MiddleName",
    "MiddleInitial",
    "Surname",
    "LastInitial",
    "SuffixGenerational",
    "SuffixOther",
    "Nickname",
    "And",
    "CorporationName",
    "CorporationNameOrganization",
    "CorporationNameAndCompany",
    "CorporationNameBranchType",
    "CorporationNameBranchIdentifier",
    "CorporationCommitteeType",
    "CorporationLegalType",
    "ShortForm",
    "ProxyFor",
    "AKA",
]

PARENT_LABEL = "Name"
GROUP_LABEL = "NameCollection"

MODEL_FILES = {
    "generic": "generic_learned_settings.crfsuite",
    "person": "person_learned_settings.crfsuite",
    "company": "company_learned_settings.crfsuite",
}
# default model file to use if user doesn't specify a model file
MODEL_FILE = MODEL_FILES["generic"]

VOWELS_Y = tuple("aeiouy")
PREPOSITIONS = {"for", "to", "of", "on"}


def _loadTagger(model_type: str) -> pycrfsuite.Tagger:
    tagger = pycrfsuite.Tagger()
    try:
        tagger.open(
            os.path.split(os.path.abspath(__file__))[0] + "/" + MODEL_FILES[model_type]
        )
    except OSError:
        tagger = None
        warnings.warn(
            "You must train the model (parserator train [traindata] [modulename]) to create the %s file before you can use the parse and tag methods"
            % MODEL_FILES[model_type]
        )

    return tagger


TAGGERS = {model_type: _loadTagger(model_type) for model_type in MODEL_FILES}

TAGGER = _loadTagger("generic")


def parse(raw_string: str, type: str | None = None) -> list[tuple[str, str]]:
    if type is None:
        type = "generic"
    tagger = TAGGERS[type]
    if not tagger:
        raise OSError(
            f"""
MISSING MODEL FILE: {MODEL_FILES[type]}
You must train the model before you can use the parse and tag methods
To train the model annd create the model file, run:
parserator train [traindata] [modulename]"""
        )

    tokens = tokenize(raw_string)
    if not tokens:
        return []

    features = tokens2features(tokens)

    tags = tagger.tag(features)
    return list(zip(tokens, tags))


def tag(raw_string: str, type: str | None = None) -> tuple[dict[str, str], str]:
    tagged = {}

    prev_label = None
    and_label = False
    proxy_label = False
    aka_label = False

    interrupting_tags = (
        "CorporationNameOrganization",
        "CorporationNameBranchType",
        "CorporationNameBranchIdentifier",
        "ProxiedCorporationNameOrganization",
        "OtherCorporationNameOrganization",
        "OtherCorporationNameBranchType",
        "OtherCorporationNameBranchIdentifier",
    )

    for token, label in parse(raw_string, type):

        if label == "And":
            and_label = True
        elif label == "AKA":
            aka_label = True
        elif label == "ProxyFor":
            proxy_label = True

        elif and_label and label in tagged:
            label = "Second" + label
        elif aka_label and label in tagged:
            label = "Other" + label
        elif proxy_label and label in tagged:
            label = "Proxied" + label

        if label not in tagged:
            tagged[label] = [token]

        elif label == prev_label or prev_label in interrupting_tags:
            tagged[label].append(token)
        elif label in interrupting_tags:
            tagged[label].append(token)

        else:
            raise RepeatedLabelError(raw_string, parse(raw_string), label)

        prev_label = label

    tagged_name = {}
    for label in tagged:
        component = " ".join(tagged[label])
        component = component.strip(" ,;")
        tagged_name[label] = component

    if "CorporationName" in tagged_name or "ShortForm" in tagged_name:
        name_type = "Corporation"
    elif and_label:
        name_type = "Household"
    else:
        name_type = "Person"

    return tagged_name, name_type


def tokenize(raw_string: str) -> list[str]:

    if isinstance(raw_string, bytes):
        raw_string = raw_string.decode()

    re_tokens = re.compile(
        r"""
    \bc/o\b
    |
    [("']*\b[^\s\/,;#&()]+\b[.,;:'")]* # ['a-b. cd,ef- '] -> ['a-b.', 'cd,', 'ef']
    |
    [#&@/]
    """,
        re.I | re.VERBOSE | re.UNICODE,
    )

    tokens = re_tokens.findall(raw_string)

    if not tokens:
        return []

    return tokens


def tokens2features(tokens) -> list[Feature]:

    feature_sequence = [tokenFeatures(tokens[0])]
    previous_features = feature_sequence[-1].copy()

    seen_comma = False

    for token in tokens[1:]:
        token_features = tokenFeatures(token)
        if not seen_comma and previous_features["comma"]:
            seen_comma = True
        if seen_comma:
            token_features["seen.comma"] = True

        current_features = token_features.copy()

        feature_sequence[-1]["next"] = current_features
        token_features["previous"] = previous_features

        feature_sequence.append(token_features)

        previous_features = current_features

    if len(feature_sequence) > 1:
        feature_sequence[0]["rawstring.start"] = True
        feature_sequence[-1]["rawstring.end"] = True
        feature_sequence[1]["previous"]["rawstring.start"] = True  # type: ignore [index]
        feature_sequence[-2]["next"]["rawstring.end"] = True  # type: ignore [index]

    else:
        feature_sequence[0]["singleton"] = True

    return feature_sequence


def tokenFeatures(token: str) -> Feature:

    if token in ("&"):
        token_clean = token_abbrev = token

    else:
        token_clean = re.sub(r"(^[\W]*)|([^.\w]*$)", "", token.lower())
        token_abbrev = re.sub(r"\W", "", token_clean)

    metaphone = doublemetaphone(token_abbrev)

    features = {
        "nopunc": token_abbrev,
        "abbrev": token_clean.endswith("."),
        "comma": token.endswith(","),
        "hyphenated": "-" in token_clean,
        "contracted": "'" in token_clean,
        "bracketed": bool(
            re.match(r'(["(\']\w+)|(\w+[")\'])', token)
            and not re.match(r'["(\']\w+[")\']', token)
        ),
        "fullbracketed": bool(re.match(r'["(\']\w+[")\']', token)),
        "length": len(token_abbrev),
        "initial": len(token_abbrev) == 1 and token_abbrev.isalpha(),
        "has.vowels": bool(set(token_abbrev[1:]) & set(VOWELS_Y)),
        "just.letters": token_abbrev.isalpha(),
        "roman": set("xvi").issuperset(token_abbrev),
        "endswith.vowel": token_abbrev.endswith(VOWELS_Y),
        "digits": digits(token_abbrev),
        "metaphone1": metaphone[0],
        "metaphone2": metaphone[1],
        "more.vowels": vowelRatio(token_abbrev),
        "in.names": token_abbrev.upper() in ratios,
        "prepositions": token_abbrev in PREPOSITIONS,
        "first.name": ratios.get(token_abbrev.upper(), 0),
        "gender_ratio": gender_names.get(token_abbrev, False),
        "possessive": token_clean.endswith("'s"),
    }

    reversed_token = token_abbrev[::-1]
    for i in range(1, len(token_abbrev)):
        features["prefix_%s" % i] = token_abbrev[:i]
        features["suffix_%s" % i] = reversed_token[:i][::-1]
        if i > 4:
            break

    for tri_gram in ngrams(token_abbrev, 3):
        features[tri_gram] = True

    for four_gram in ngrams(token_abbrev, 4):
        features[four_gram] = True

    return features


def vowelRatio(token: str) -> int | bool:
    n_chars = len(token)
    if n_chars > 1:
        n_vowels = sum(token.count(c) for c in VOWELS_Y)
        return int(n_vowels // float(n_chars))
    else:
        return False


def digits(token: str) -> typing.Literal["all_digits", "some_digits", "no_digits"]:
    if token.isdigit():
        return "all_digits"
    elif set(token) & set(string.digits):
        return "some_digits"
    else:
        return "no_digits"


def ngrams(word: str, n: int = 2) -> typing.Generator[str]:
    return ("".join(letters) for letters in zip(*[word[i:] for i in range(n)]))


class RepeatedLabelError(probableparsing.RepeatedLabelError):
    REPO_URL = "https://github.com/datamade/probablepeople/issues/new"
    DOCS_URL = "https://probablepeople.readthedocs.io/"
