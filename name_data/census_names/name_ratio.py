import csv
import pprint

given_names = {}

with open("dist.female.first") as f:
    f.next()
    for row in f:
        row = row.split()
        name = row[0]
        proportion = float(row[1]) / 100
        given_names[name] = proportion

with open("dist.male.first") as f:
    f.next()
    for row in f:
        row = row.split()
        name = row[0]
        proportion = float(row[1]) / 100
        if name in given_names:
            given_names[name] += proportion
        else:
            given_names[name] = proportion

surnames = {}

with open("app_c.csv") as f:
    reader = csv.reader(f)
    reader.next()
    for row in reader:
        name = row[0]
        proportion = float(row[3]) / 100000
        surnames[name] = proportion

names = {}

for name in given_names.keys() & surnames.keys():
    prop_given = given_names[name]
    prop_sur = surnames[name]

    names[name] = prop_given / (prop_given + prop_sur)

for name in given_names.keys() - surnames.keys():
    names[name] = 1

for name in surnames.keys() - given_names.keys():
    names[name] = 0


with open("ratios.py", "w") as f:
    f.write(pprint.pformat(names, indent=4))
