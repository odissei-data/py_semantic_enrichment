from xml_parser import formatXML
from gen_dict_extract import gen_dict_extract
from xml.etree import cElementTree as ET

def main(xml):
    source = xml.strip()
    tree = ET.ElementTree(ET.fromstring(source))
    root = tree.getroot()
    keys = ['title', 'subject', 'creatorName', 'language', 'identifier', 'coverage', 'description']
    data = formatXML(root)
    output = dict()
    for key in keys:
        dict_data = gen_dict_extract(key, data)
        for i in dict_data:
            if isinstance(i, str):
                if 'subj' in key and ',' in i:
                    subs = i.split(',')
                    for sub in subs:
                        new_sub = sub.strip()
                        output.setdefault(key, [])
                        output[key].append(new_sub)
                else:
                    output.setdefault(key, [])
                    output[key].append(i)

    return output
