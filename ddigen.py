from merger import termurimatch
from main import main
from rdflib.namespace import FOAF, DCTERMS, XSD, RDF, SDO, SKOS
from rdflib import Graph, Namespace, URIRef, BNode, Literal
import nltk

def ddigenerator(xml):
    #Fetching the relevant content of the XML File from other functions
    content = main(xml)
    title = content['title'][0].replace(' ', '_')
    titleuri = URIRef(content['identifier'][0])
    name = content['identifier'][0].split(':')[-1]
    try:
        language = content['language'][0]
    except:
        language = 'nl'
    ###
    g = Graph()
    #The following terms are namespaces for DDI Discovery
    disco = Namespace('http://rdf-vocabulary.ddialliance.org/discovery#')
    skos = Namespace('http://www.w3.org/2004/02/skos/core#')
    dcterms = Namespace('http://purl.org/dc/terms/')
    ddi = Namespace('https://rdf-vocabulary.ddialliance.org')
    oai = Namespace('https://easy.dans.knaw.nl/oai/oai:easy.dans.knaw.nl:easy-dataset:')
    adms = Namespace('https://rdf-vocabulary.ddialliance.org/discovery.html#adms')
    dbpedia = Namespace('http://dbpedia.org/resource/')
    rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema#')
    #Binding the namespaces to strings
    g.bind('disco', disco)
    g.bind('skos', skos)
    g.bind('dcterms', dcterms)
    g.bind('ddi', oai)
    g.bind('adms', adms)
    g.bind('dbpedia', dbpedia)
    g.bind('rdfs', rdfs)
    ###
    #Iterating over the URI's from the translated terms
    iter = termurimatch(content)
    g.add((oai.Study_1,RDF.type,disco.study))
    for triple in iter:
        type = triple[0]
        spec = triple[1]
        uri = triple[2]
        if 'title' in type:
            g.add((oai.Study_1, dcterms.title, Literal(content['title'][0], lang = language)))
            g.add((oai.Study_1, dcterms.identifier, Literal(name)))
        elif 'creatorName' in type:
            #Since some creator tags have identifiers in them I will first put it through some NLTK NLP
            wordonly = []
            for i in nltk.word_tokenize(content['creatorName'][0]):
                if i.isalpha():
                    wordonly.append(i)
                    spec = ' '.join(wordonly)
            g.add((oai.Study_1, dcterms.creator, Literal(content['creatorName'][0])))
        elif 'creator' in type:
            #Because sometimes the creator tag is used instead
            wordonly = []
            for i in nltk.word_tokenize(content['creator'][0]):
                if i.isalpha():
                    wordonly.append(i)
                    spec = ' '.join(wordonly)
            g.add((oai.Study_1, dcterms.creator, Literal(content['creator'][0])))
        elif 'coverage' in type:
        #Since coverage tag can contain both date, and location, i'm filtering for this here
            #Checking for location
            if spec.isalpha():
                g.add((dcterms.spatial, RDF.type, dcterms.Location))
                g.add((dcterms.spatial, rdfs.label, Literal(content['coverage'][0], lang = language)))
            #Checking for date
            if spec[0].isnumeric():
                splitters = ['-', ',', ':', '_', '*', ';']
                for i in splitters:
                    if i in spec:
                        starttoend = spec.split(i)
                    else:
                        continue
                g.add((dcterms.temporal, RDF.type, dcterms.PeriodOfTime))
                g.add((dcterms.temporal, disco.startDate, Literal(starttoend[0])))
                g.add((dcterms.temporal, disco.endDate, Literal(starttoend[-1])))
        #Because for some studies, the temporal coverage can also be found in the subject tag
        for subject in content['subject']:
            if 'temporal coverage:' in subject.lower():
                startone = subject.lower().split(':')
                altsplit = ['-', ',', ':', '_', '*', ';', '=']
                for split in altsplit:
                    if split in startone[1]:
                        starttoend = startone[1].split(split)
                g.add((dcterms.temporal, RDF.type, dcterms.PeriodOfTime))
                g.add((dcterms.temporal, disco.startDate, Literal(starttoend[-2])))
                g.add((dcterms.temporal, disco.endDate, Literal(starttoend[-1])))
        if not uri == None and 'subj' in type:
            uri = URIRef(triple[2])
            g.add((oai.Study_1,dcterms.subject,uri))
        g.add((oai.Study_1,dcterms.abstract,Literal(content['description'][0], lang = language)))
    result = g.serialize(format='turtle').decode('u8')
    return result
