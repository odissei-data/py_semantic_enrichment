import nltk

def formatXML(parent):
    """
    Recursive operation which returns a tree formatted
    as dicts and lists.
    Decision to add a list is to find the 'List' word
    in the actual parent tag.
    """
    ret = {}
    tag_tokens = nltk.word_tokenize(parent.tag)
    if parent.items():
        ret.update(dict(parent.items()))
    if parent.text:
        ret[tag_tokens[-1]] = parent.text
    if 'List' in parent.tag:
        ret['__list__'] = []
        for element in parent:
            ret['__list__'].append(formatXML(element))
    else:
        for element in parent:
            elem_tokens = nltk.word_tokenize(element.tag)
            ret.setdefault(elem_tokens[-1], [])
            ret[elem_tokens[-1]].append(formatXML(element))
    return ret
