from SPARQLWrapper import SPARQLWrapper, JSON
from main import main
import googletrans

def translator(xml):
    stdict = xml
    stdict_translated = dict()
    translator = googletrans.Translator()
    for key, value in stdict.items():
        if 'lang' in key:
            language = value[0]
        else:
            language = 'nl'
    for key, value in stdict.items():
        stdict_translated.setdefault(key, [])
        if not 'identifier' in key and not 'description' in key:
            for i in value:
                try:
                    translated = translator.translate(i, src=language, dest ='en')
                    stdict_translated[key].append(translated.text)
                except:
                    pass
    return stdict_translated

###
def termurimatch(xml):
    terms = translator(xml)
    result = []
    for key, value in terms.items():
        for i in value:
            try:
                tuple = (key, i, geturi(i))
            except:
                pass
            result.append(tuple)
    return result

def get_description(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)  # the previous query as a literal string
    return sparql.query().convert()


def geturi(word):
    '''This function fetches the URI from DBPedia.
    :word: This is the term to look for when fetching the URI'''
    qry ="""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX dbo: <http://dbpedia.org/ontology/>

    SELECT ?s WHERE {
    {
    ?s rdfs:label '"""+word+"""'@en ;
       a owl:Thing .
    }
    UNION
    {
    ?altName rdfs:label '"""+word+"""'@en ;
        dbo:wikiPageRedirects ?s .
    }
    }"""
    search = get_description(qry)
    for i in search['results']['bindings']:
        return i['s']['value']
