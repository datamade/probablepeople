import re
import string


######### TOKEN CONFIG #########

# some config on how to split a string into tokens
# - set characters to split on?
# - set characters to append at the end of tokens?


######### LABEL CONFIG #########

# these are the labels for tagging tokens
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

######## XML CONFIG ############

# this is the tag for each string
PARENT_LABEL = 'Name'

# this is the tag for a group of strings
GROUP_LABEL = 'NameCollection'


######## FEATURE CONFIG ########

def tokenFeatures(token) :

    if token in (u'&', u'#') :
        token_clean = token
    else :
        token_clean = re.sub(r'(^[\W]*)|([^.\w]*$)', u'', token)
    token_chars = re.sub(r'[\W]', u'', token_clean.lower())

    features = {'nopunc' : token_chars,
                'is.abbrev' : bool(re.match('(\w\.)+', token_clean)),
                'is.initial' : bool(re.match('(\w\.)', token_clean)),
                'case' : casing(token_clean),
                'length' : (u'w:' + unicode(len(token_chars))),
                'endsinpunc' : (token[-1]
                                if bool(re.match('[^\w]', token[-1]))
                                else False),
                'has.punc' : (True
                                if bool(re.match('.*[^\w].*', token))
                                else False),
                'punc' :    (re.sub(r'\w', u'', token)
                                if bool(re.match('.*[^\w].*', token))
                                else False),
                'has.vowels'  : bool(set(token_chars[1:]) & set('aeiou')),
                'first1char' : (token_chars[0] if len(token_chars) > 0
                                else False),
                'first2char' : (token_chars[:2] if len(token_chars) > 1
                                else False)
                }

    return features

def casing(token) :
    if token.isupper() :
        return 'upper'
    elif token.islower() :
        return 'lower' 
    elif token.istitle() :
        return 'title'
    else :
        return 'other'
