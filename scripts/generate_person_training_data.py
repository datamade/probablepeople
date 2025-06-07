import random
import xml.etree.ElementTree as ET

from faker import Faker

# Paths
FILE_PATH = "name_data/labeled/person_labeled.xml"
NUM_RECORDS_TO_ADD = 1000  # number of records to add

# Load existing XML
tree = ET.parse(FILE_PATH)
root = tree.getroot()

fake = Faker()

suffixes = [None, "Jr.", "Sr.", "II", "III", "IV"]

for _ in range(NUM_RECORDS_TO_ADD):
    first = fake.first_name()
    last = fake.last_name()
    # optional middle name or initial
    mid_type = random.choice(["none", "name", "initial"])
    if mid_type == "name":
        mid = fake.first_name()
    elif mid_type == "initial":
        mid = f"{fake.first_name()[0]}."
    else:
        mid = None
    # optional suffix
    suffix = random.choice(suffixes)

    name_el = ET.Element("Name")
    # GivenName
    gn = ET.SubElement(name_el, "GivenName")
    gn.text = first
    # MiddleName / MiddleInitial
    if mid:
        if len(mid) == 2 and mid.endswith("."):
            mi = ET.SubElement(name_el, "MiddleInitial")
            mi.text = mid
        else:
            mm = ET.SubElement(name_el, "MiddleName")
            mm.text = mid
    # Surname
    sn = ET.SubElement(name_el, "Surname")
    sn.text = last
    # SuffixGenerational
    if suffix:
        sg = ET.SubElement(name_el, "SuffixGenerational")
        sg.text = suffix

    root.append(name_el)

# Write back
tree.write(FILE_PATH, encoding="utf-8", xml_declaration=True)
