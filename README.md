# py_semantic_enrichment
Transform DANS Easy XML data into semantically enriched RDF data based on DISCO-DDI and DBPedia



# CMM
This is a repository that runs a RESTful API on a nginx server. Transforming xml-based study metadata into DBPedia linked DDI-RDF data

myproject.py is the code that runs the server using the Flask module and calls all the other code.

In main.py all the XML parsing is done and in and ddigen.py creates the DDI template and adds the enriched data to that template. 
Project commissioned by ODISSEI, working with DANS-EASY data.

https://odissei-data.nl/nl/
https://dans.knaw.nl/nl

The code is a result from a "DH in Practice" project at the VU Amsterdam executed by Liska Suckau, Felix den Heijer and Gijs Timmerij and supervised by Ronald Siebes

