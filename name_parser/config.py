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