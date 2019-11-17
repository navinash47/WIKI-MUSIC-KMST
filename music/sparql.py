
import logging
import rdflib
from rdflib.graph import Graph, URIRef
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib.plugins.memory import IOMemory
import pandas as pd
import os
import sys


# configuring logging
logging.basicConfig() 


def con1(query):
# configuring the end-point and constructing query
    sparql = SPARQLWrapper("http://dbtune.org/musicbrainz/sparql")
    construct_query="""
            PREFIX mo: <http://purl.org/ontology/mo/>
            PREFIX mbz: <http://purl.org/ontology/mbz#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>    
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX bio: <http://purl.org/vocab/bio/0.1/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX tags: <http://www.holygoat.co.uk/owl/redwood/0.1/tags/>
            PREFIX geo: <http://www.geonames.org/ontology#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX lingvoj: <http://www.lingvoj.org/ontology#>
            PREFIX rel: <http://purl.org/vocab/relationship/>
            PREFIX vocab: <http://dbtune.org/musicbrainz/resource/vocab/>
            PREFIX event: <http://purl.org/NET/c4dm/event.owl#>
            PREFIX map: <file:/home/moustaki/work/motools/musicbrainz/d2r-server-0.4/mbz_mapping_raw.n3#>
            PREFIX db: <http://dbtune.org/musicbrainz/resource/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            SELECT DISTINCT ?v1 ?v2 ?v3 
            WHERE{ 
                    ?r rdfs:label \""""
    construct_query=construct_query+query
    construct_query=construct_query+"""\".
                    ?r dc:description ?v1 .
                    ?r foaf:homepage ?v2 .
                    ?r rdf:type ?v3 .
                    }
            LIMIT 10"""

    
    sparql.setQuery(construct_query)
    sparql.setReturnFormat(JSON)
    a=sparql.query().convert()
    b=a["results"]["bindings"]
    all=[]
    if(len(b)!=0):
        des=(b[0])["v1"]["value"]
        home=(b[0])["v2"]["value"]    
        typ=(b[0])["v3"]["value"]
        
        all.append(des)
        all.append(home)
        all.append(typ)
    return all,(len(b)==0)
def con2(query):
    sparql = SPARQLWrapper("http://dbtune.org/musicbrainz/sparql")
    c1="""
             PREFIX mo: <http://purl.org/ontology/mo/>
             PREFIX mbz: <http://purl.org/ontology/mbz#>
             PREFIX owl: <http://www.w3.org/2002/07/owl#>    
             PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
             PREFIX bio: <http://purl.org/vocab/bio/0.1/>
             PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
             PREFIX tags: <http://www.holygoat.co.uk/owl/redwood/0.1/tags/>
             PREFIX geo: <http://www.geonames.org/ontology#>
             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
             PREFIX lingvoj: <http://www.lingvoj.org/ontology#>
             PREFIX rel: <http://purl.org/vocab/relationship/>
             PREFIX vocab: <http://dbtune.org/musicbrainz/resource/vocab/>
             PREFIX event: <http://purl.org/NET/c4dm/event.owl#>
             PREFIX map: <file:/home/moustaki/work/motools/musicbrainz/d2r-server-0.4/mbz_mapping_raw.n3#>
             PREFIX db: <http://dbtune.org/musicbrainz/resource/>
             PREFIX foaf: <http://xmlns.com/foaf/0.1/>
             PREFIX dc: <http://purl.org/dc/elements/1.1/>
             SELECT DISTINCT ?v ?f ?img
             WHERE { 
                     ?r rdfs:label \""""
    c1=c1+query
    c1=c1+"""\" .
                     ?v foaf:maker ?r  .
                     ?v dc:title ?f .
                     ?v vocab:albummeta_coverarturl ?img
                     }
             ORDER BY ?v
"""
    sparql.setQuery(c1)
    sparql.setReturnFormat(JSON)
    a=sparql.query().convert()
    b=a["results"]["bindings"]
    v=[]
    title=[]
    img=[]
    
    for i in range(len(b)):
        v.append((b[i])["v"]["value"])
        title.append((b[i])["f"]["value"])
        img.append((b[i])["img"]["value"])
      
    db="http://dbtune.org/musicbrainz/resource/"
    count=20
    R=[]
    for j in range(len(v)):
        w=v[j]
        if(w[len(db)]=='r' and count!=0):
            t=[]
            t.append(v[j])
            t.append(title[j])
            t.append(img[j])
            R.append(t)
            print(title[j])
            count=count-1
    
    return R,v

def con3(query):
    sparql = SPARQLWrapper("http://dbtune.org/musicbrainz/sparql")
    print(query)
    construct_query="""
            PREFIX mo: <http://purl.org/ontology/mo/>
            PREFIX mbz: <http://purl.org/ontology/mbz#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>    
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX bio: <http://purl.org/vocab/bio/0.1/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX tags: <http://www.holygoat.co.uk/owl/redwood/0.1/tags/>
            PREFIX geo: <http://www.geonames.org/ontology#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX lingvoj: <http://www.lingvoj.org/ontology#>
            PREFIX rel: <http://purl.org/vocab/relationship/>
            PREFIX vocab: <http://dbtune.org/musicbrainz/resource/vocab/>
            PREFIX event: <http://purl.org/NET/c4dm/event.owl#>
            PREFIX map: <file:/home/moustaki/work/motools/musicbrainz/d2r-server-0.4/mbz_mapping_raw.n3#>
            PREFIX db: <http://dbtune.org/musicbrainz/resource/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            SELECT DISTINCT  ?v1 ?v2 ?v3 ?v4 
            WHERE { 
            ?r rdfs:label \""""
    construct_query=construct_query+query
    construct_query=construct_query+"""\" .
            ?r dc:title ?v1 .
            ?r mo:track_number ?v2 .
            ?r foaf:maker ?v3 .
            ?v3 rdfs:label ?v4
            }
            ORDER BY ?v2 ?v4
            LIMIT 100"""

    
    sparql.setQuery(construct_query)
    sparql.setReturnFormat(JSON)
    a=sparql.query().convert()
    b=a["results"]["bindings"]
    
    Art=[]
    t_no=[]
    url=[]
    for m in b:
        Art.append(m["v4"]["value"])
        t_no.append(m["v2"]["value"])
        url.append(m["v3"]["value"])
        
    d=[]
    d=pd.unique(Art)
    Albums=[]
    for i in range(len(d)):
        Temp=[]
        for j in range(len(Art)):
            if(Art[j]==d[i]):
                t=[]
                t.append(Art[j])
                t.append(t_no[j])
                t.append(url[j])
                Temp.append(t)
        Albums.append(Temp)
        
    return Albums[0:19]

def con4(query):
    sparql = SPARQLWrapper("http://dbtune.org/musicbrainz/sparql")
    print(query)
    construct_query="""
            PREFIX mo: <http://purl.org/ontology/mo/>
            PREFIX mbz: <http://purl.org/ontology/mbz#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>    
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX bio: <http://purl.org/vocab/bio/0.1/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX tags: <http://www.holygoat.co.uk/owl/redwood/0.1/tags/>
            PREFIX geo: <http://www.geonames.org/ontology#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX lingvoj: <http://www.lingvoj.org/ontology#>
            PREFIX rel: <http://purl.org/vocab/relationship/>
            PREFIX vocab: <http://dbtune.org/musicbrainz/resource/vocab/>
            PREFIX event: <http://purl.org/NET/c4dm/event.owl#>
            PREFIX map: <file:/home/moustaki/work/motools/musicbrainz/d2r-server-0.4/mbz_mapping_raw.n3#>
            PREFIX db: <http://dbtune.org/musicbrainz/resource/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            SELECT DISTINCT ?v2 ?v4 ?album
            WHERE { 
            ?r rdfs:label \""""
    construct_query=construct_query+query
    construct_query=construct_query+"""\" .
            ?r mo:published_as ?v1 .
            ?v1 mo:track_number ?v2 .
            ?v1 foaf:maker ?v3 .
            ?v3 rdfs:label ?v4 .
            ?v5 mo:track ?v1 .
            ?v5 dc:title ?album
            }
            ORDER BY ?v4
            """
    sparql.setQuery(construct_query)
    sparql.setReturnFormat(JSON)
    a=sparql.query().convert()
    b=a["results"]["bindings"]
    
    Art=[]
    t_no=[]
    Alb=[]
    for m in b:
        Art.append(m["v4"]["value"])
        t_no.append(m["v2"]["value"])
        Alb.append(m["album"]["value"])
    
    art=[]
    p=[]
    if(len(Alb)!=0):
        p.append(Alb[0])
        p.append(t_no[0])
        p.append(Art[0])
        art.append(p)
        for i in range(1,len(Art)):
            if(Art[i]!=Art[i-1]):
                p=[]
                p.append(Alb[i])
                p.append(t_no[i])
                p.append(Art[i])
                art.append(p)
                
    return art



            
 