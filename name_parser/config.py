######### TOKEN CONFIG #########

# some config on how to split a string into tokens
# - set characters to split on?
# - set characters to append at the end of tokens?


######### LABEL CONFIG #########

# these are the labels for tagging tokens
LABELS = [
'PrefixMarital',       # prefix types? e.g. title?
'PrefixOther',
'GivenName',
'FirstInitial', # should name & initial be separate tags
'MiddleName',
'MiddleInitial',
'Surname',
'LastInitial',
'SuffixGenerational',       # suffix types?
'SuffixOther',
'Nickname'
]

NULL_LABEL = 'Null'