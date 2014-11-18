import name_parser
from lxml import etree

# given a list of labeled sequences to an xml list, 
# appends corresponding xml to existing xml
# format for list_to_append:    [   [ (token, label), (token, label), ...],
#                                   [ (token, label), (token, label), ...],
#                                   [ (token, label), (token, label), ...],
#                                   ...           ]
# calls sequence2XML
# called by appendListToXMLfile
def appendListToXML(list_to_append, collection_XML) :
    for labeled_sequence in list_to_append:
        sequence_xml = sequence2XML(labeled_sequence)
        collection_XML.append(sequence_xml)
    return collection_XML


# given a labeled sequence in the form of [(token, label), (token, label), ...]
# generates xml for that sequence
# called by appendListToXML
def sequence2XML(labeled_sequence) :
    parent_tag = name_parser.config.PARENT_LABEL
    sequence_xml = etree.Element(parent_tag)
    for token, label in labeled_sequence:
        component_xml = etree.Element(label)
        component_xml.text = token
        component_xml.tail = ' '
        sequence_xml.append(component_xml)
    sequence_xml[-1].tail = ''
    return sequence_xml


# formatting for an xml collection
def stripFormatting(collection) :
    collection.text = None 
    for element in collection :
        element.text = None
        element.tail = None
        
    return collection


# appends a labeled list to an xml file
# calls appendListToXML, stripFormatting
def appendListToXMLfile(labeled_list, filepath):

    if os.path.isfile(filepath):
        with open( filepath, 'r+' ) as f:
            tree = etree.parse(filepath)
            collection_XML = tree.getroot()
            collection_XML = stripFormatting(collection_XML)

    else:
        collection_tag = name_parser.config.GROUP_LABEL
        collection_XML = etree.Element(collection_tag)


    collection_XML = appendListToXML(labeled_list, collection_XML)


    with open(filepath, 'w') as f :
        f.write(etree.tostring(collection_XML, pretty_print = True)) 


# writes strings to a file
def list2file(string_list, filepath):
    file = open( filepath, 'w' )
    for string in string_list:
        file.write('"%s"\n' % string)