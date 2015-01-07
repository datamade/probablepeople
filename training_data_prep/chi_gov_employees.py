import csv
import random

if __name__ == '__main__' :

    raw_csv = '../name_data/unlabeled/Current_Employee_Names__Salaries__and_Position_Titles.csv'
    outfile = '../name_data/unlabeled/chi_gov_employees.csv'

    with open(raw_csv, 'rU') as f:
        reader = csv.reader(f)
        tagged_data = [row[0] for row in reader]
    
    random.shuffle(tagged_data)

    with open(outfile, "wb") as f:
        writer = csv.writer(f)
        for name in tagged_data:
            writer.writerow([name])
