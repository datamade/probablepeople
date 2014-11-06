######### TOKEN CONFIG #########

# some config on how to split a string into tokens
# - set characters to split on?
# - set characters to append at the end of tokens?


######### LABEL CONFIG #########

# these are the labels for tagging tokens
LABELS = [
'Prefix',       # prefix types? e.g. title?
'FirstName',
'FirstInitial', # should name & initial be separate tags
'MiddleName',
'MiddleInitial',
'LastName',
'LastInitial',
'Suffix',       # suffix types?
'Nickname'
]

NULL_LABEL = 'Null'