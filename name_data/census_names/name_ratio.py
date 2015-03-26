from __future__ import division, unicode_literals, print_function
from future.utils import viewkeys

import csv
import pprint

given_names = {}

with open("dist.female.first") as f :
    f.next()
    for row in f :
        row = row.split()
        name = row[0]
        proportion = float(row[1])/100
        given_names[name] = proportion

with open("dist.male.first") as f :
    f.next()
    for row in f :
        row = row.split()
        name = row[0]
        proportion = float(row[1])/100
        if name in given_names :
            given_names[name] += proportion
        else :
            given_names[name] = proportion

surnames = {}

with open("app_c.csv") as f :
    reader = csv.reader(f)
    reader.next()
    for row in reader :
        name = row[0]
        proportion = float(row[3])/100000
        surnames[name] = proportion

names = {}

for name in viewkeys(given_names) & viewkeys(surnames) :
    prop_given = given_names[name]
    prop_sur = surnames[name]

    names[name] = prop_given / (prop_given + prop_sur)

for name in viewkeys(given_names) - viewkeys(surnames) :
    names[name] = 1

for name in viewkeys(surnames) - viewkeys(given_names) :
    names[name] = 0



with open("ratios.py", 'w') as f:
    f.write(pprint.pformat(names, indent=4))


