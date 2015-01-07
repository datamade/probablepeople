import csv
import random
import re

def first_col_to_csv(raw_csv, outfile):

    with open(raw_csv, 'rU') as f:
        reader = csv.reader(f)
        tagged_data = [row[0] for row in reader]
    
    random.shuffle(tagged_data)

    with open(outfile, "wb") as f:
        writer = csv.writer(f)
        for name in tagged_data:
            writer.writerow([name])

def filtered_names_to_csv(infile, outfile, regex_patterns):

    with open(infile, 'rU') as f:
        reader = csv.reader(f)
        names = [row[0] for row in reader]

    tricky_names = [name for name in names if not regex_pattern.match(name)]

    with open(outfile, "wb") as f:
        writer = csv.writer(f)
        for name in tricky_names:
            writer.writerow([name])

    

if __name__ == '__main__' :

    raw_csv = '../name_data/unlabeled/Current_Employee_Names__Salaries__and_Position_Titles.csv'
    outfile = '../name_data/unlabeled/chi_gov_employees.csv'

    # first_col_to_csv(raw_csv, outfile)

    unlabeled_chi_gov_names = '../name_data/unlabeled/unlabeled_chi_gov_employees.csv'
    tricky_name_csv = '../name_data/unlabeled/tricky_chi_gov_names.csv'
    regex_pattern = re.compile(r'(^\S+,\s\s\w+$)|(^\S+,\s\s\w+\s\w$)', re.IGNORECASE)

    filtered_names_to_csv(unlabeled_chi_gov_names, tricky_name_csv, regex_pattern)
