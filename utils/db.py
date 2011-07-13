#Copyright (C) 2011 Iraide Diaz (sharem)
#Copyright (C) 2011 Xabier Larrakoetxea (slok)
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>. 
import rdflib
from rdflib import plugin
from rdflib.store import Store
from rdflib import Namespace
from rdflib import Literal
from rdflib import URIRef
from rdflib.store import SQLite
from rdflib.store import Store
from rdflib.graph import *
from rdflib.namespace import Namespace
from rdflib.query import *
from rdflib import sparql
from rdflib.query.result import QueryResult

def store_RDF(rdfPath, user, password, db):
    """Stores an RDF file (path or URL) in the Database
    Keyword arguments:
    rdfPath -- the RDF file path, could be a System path or a URL
    user -- The user for accesing the DB
    password -- The password of the user for accesing the DB
    db -- The DB that we are going to access
    """
    #config string: host=localhost,user=XXXX,password=YYYYYYYYY,db=ZZZZZ
    #Making the configuration string
    configString = "host=localhost,user="
    configString += user
    configString += ",password="
    configString += password
    configString += ",db="
    configString += db
    #connect to database
    store = plugin.get('MySQL', Store)(db)

    #Try to open a created DB, if there isn't catch the exception to
    #create a new one
    try:
        store.open(configString,create=False)
    except:
        store.open(configString,create=True)

    graph = Graph(store)
    #Parse the path to the RDF
    graph.parse(rdfPath)
    #Commit the changes(insert, delete and modifications in to the database)
    graph.commit()

    print("[OK] RDF stored in Database")
    graph.close()

#####################################################################################
def sparql_prefix_parser(query):
    """ Parses a "PREFIX" line(s) from a query to obtain all the 
    variable=url in that line, the strings have to be like this:
    #PREFIX ex1:  <http://www.example.org/schemas/Concept1>
    only is possible to parse "PREFIX" in capital letters
    Keyword arguments:
    query -- the query to parse
    
    Returns a list made of [variable,url] values
    """
    returnList = []
    while query.count("PREFIX") != 0:
        #get caracters between X and Y-> [X:Y], so we search the characters
        variable = query[query.find("PREFIX")+len("PREFIX"):query.find(":")]
        url = query[query.find("<")+1:query.find(">")]

        #replace spaces (blanks)
        variable = variable.replace(" ", "")
        url = url.replace(" ","")

        #add to the list
        returnList.append([variable,url])

        #delete from the beggining (PREFIX) to the first ">"
        query = query.replace(query[0:query.find(">")+1], ' ', 1)
    return returnList
#####################################################################################
def delete_sparql_prefix(query):
    """ Deletes the PREFIX line(s) from the query and returns it
    """
    while query.count("PREFIX") != 0:
        query = query.replace(query[0:query.find(">")+1], '', 1)

    return query
#####################################################################################
def sparql_query(query, user, password, db, output):
    """ Makes a sparql query to the SQLite database and returns a result
    Keyword arguments:
    query -- the query to execute
    user -- The user for accesing the DB
    password -- The password of the user for accesing the DB
    db -- The DB that we are going to access
    output -- the output type could be: xml, json or python object
    
    Returns a result (rdflib result)
    """	
    prefixes = {}
    #config string: host=localhost,user=XXXX,password=YYYYYYYYY,db=ZZZZZ
    #Making the configuration string
    configString = "host=localhost,user="
    configString += user
    configString += ",password="
    configString += password
    configString += ",db="
    configString += db
    #connect to database
    store = plugin.get('MySQL', Store)(db)
    #Try to open a created DB, if there isn't catch the exception to
    #create a new one
    try:
        store.open(configString,create=False)
    except:
        store.open(configString,create=True)
        
    #load the graph
    g = ConjunctiveGraph(store)

    #register the sparql and Mysqlite plugin for the queries
    plugin.register('MySQL', Store, 'rdflib.store.MySQL', 'MySQL')
    plugin.register('sparql', sparql.Processor,
         'rdflib.sparql.bison.Processor', 'Processor')
    plugin.register('SPARQLQueryResult', QueryResult,
      'rdflib.sparql.QueryResult', 'SPARQLQueryResult')

    # add prefixes to the dictionary
    for prefix in sparql_prefix_parser(query):
        prefixes[prefix[0]] = prefix[1]

    #delete PREFIX lines
    query = delete_sparql_prefix(query)

    #execute query
    qres = g.query(query, initNs=prefixes)

    #close DB
    g.close()
    
    #select the type of output
    
    if output == 'xml':
        qres = qres.serialize('xml')
    elif output == 'json':
        qres = qres.serialize('json')
    else:
        qres = qres.serialize('python')

    return qres
#####################################################################################
"""def store_ontology(rdfPath):
    """#Stores an ontology (RDF) file (path or URL) in the Database
    #Keyword arguments:
    #rdfPath -- the RDF file path, could be a System path or a URL
"""
    configString = "host=localhost,user=root,password=larrakoetxea,db=rdfstore"
    #connect to database
    store = plugin.get('MySQL', Store)('rdfstore')
    
    try:
        store.open(configString,create=False)
    except:
        store.open(configString,create=True)

    graph = Graph(store)
    #Parse the path to the RDF
    graph.parse(rdfPath)
    #Commit the changes(insert, delete and modifications in to the database)
    graph.commit()

    print("[OK] Ontology stored in Database")
    graph.close()
"""

