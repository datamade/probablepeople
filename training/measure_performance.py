from probablepeople import parse


test_strings = [
    ('Cathy Deng', ['GivenName', 'Surname']),
    ('Mr & Mrs Bob Belcher', ['PrefixMarital', 'And', 'PrefixMarital', 'GivenName', 'Surname']),
    ('Belcher, Bob', ['Surname', 'GivenName']),
    ('Bob B', ['GivenName', 'LastInitial']),
    ('Bob B.', ['GivenName', 'LastInitial']),
    ('mr bob b', ['PrefixMarital', 'GivenName', 'LastInitial']),
    ('bob b jr', ['GivenName', 'LastInitial', 'SuffixGenerational']),
    ('Bob Belcher, II', ['GivenName', 'Surname', 'SuffixGenerational']),
    ('bob belcher IV', ['GivenName', 'Surname', 'SuffixGenerational']),
    ('Bob Belcher M.D.', ['GivenName', 'Surname', 'SuffixOther']),
    ('Dr. Bob Belcher', ['PrefixOther', 'GivenName', 'Surname']),
    ('Bob Belcher PhD', ['GivenName', 'Surname', 'SuffixOther']),
    ('B Belcher', ['FirstInitial', 'Surname']),
    ('b. belcher', ['FirstInitial', 'Surname']),
    ('b belcher', ['FirstInitial', 'Surname']),
    ("Bob O'Malley", ['GivenName', 'Surname']),
    ("Bob 'Bill' O'Malley", ['GivenName', 'Nickname', 'Surname']),
    ("Bob (Bill) O'Malley", ['GivenName', 'Nickname', 'Surname']),
    ("B O'Malley", ['FirstInitial', 'Surname']),
    ('vincent van gogh', ['GivenName', 'Surname', 'Surname']),
    ('Vincent van Gogh', ['GivenName', 'Surname', 'Surname']),
    ('Anthony van Dyck', ['GivenName', 'Surname', 'Surname']),
    ('Edwin van der Sar', ['GivenName', 'Surname', 'Surname', 'Surname']),
    ('Joost van den Vondel', ['GivenName', 'Surname', 'Surname', 'Surname']),
    ('Monique van de Ven', ['GivenName', 'Surname', 'Surname', 'Surname']),
    ('Robert J. Van de Graaff', ['GivenName', 'MiddleInitial', 'Surname', 'Surname', 'Surname']),
    ('a. b. smith', ['FirstInitial', 'MiddleInitial', 'Surname']),
    ('a. bob smith', ['FirstInitial', 'MiddleName', 'Surname']),
    ('bob a and linda b belcher', ['GivenName', 'MiddleInitial', 'And', 'GivenName', 'MiddleInitial', 'Surname']),
    ('a. smith', ['FirstInitial', 'Surname']),
    ('a smith', ['FirstInitial', 'Surname']),
    ('a smith d.o.', ['FirstInitial', 'Surname', 'SuffixOther']),
    ('a smith iii', ['FirstInitial', 'Surname', 'SuffixGenerational']),
    ('a smith DO', ['FirstInitial', 'Surname', 'SuffixOther']),
    ('belcher, bob b', ['Surname', 'GivenName', 'MiddleInitial']),
    ('belcher, bob b jr', ['Surname', 'GivenName', 'MiddleInitial', 'SuffixGenerational']),
    ('Belcher, Bob B. IV', ['Surname', 'GivenName', 'MiddleInitial', 'SuffixGenerational']),
]

failed = 0
for string_tuple in test_strings :
    labels_true = string_tuple[1]
    parsed = parse(string_tuple[0])
    labels_pred = [ token[1] for token in parsed ]
    if labels_pred == labels_true:
        print string_tuple[0], "...ok"
    else:
        failed += 1
        print "*"*40
        print string_tuple[0], "...INCORRECT PARSING"
        print "pred: ", labels_pred
        print "true: ", labels_true
        print "-"*40

print "Failed", failed, "out of", len(test_strings), "strings"