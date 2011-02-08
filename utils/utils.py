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
import urllib2

#####################################################################################
def download_file(url, destination):
    """Gets a file from an URL and stores in a destination
    Keyword arguments:
    url -- The url of the file to download
    destination -- The path to store the downloaded file
    """
    #get the file from Internet
    tempFile = urllib2.urlopen(url)
    parts = []
    #split the URL(we want to get the last part(file name))
    for part in url.split('/'):
        parts.append(part)
    
    if parts[len(parts)-1] == '' :
        raise Exception, "The URL has to point to a concrete file"
    else:
        #add to the destination the last part of the splitted url (length -1)
        destination += parts[len(parts)-1]
        #open the destination file (with wb flags) and writes the "buffer"
        output = open(destination, 'wb')
        output.write(tempFile.read())
        #close the opened file
        output.close()
#####################################################################################
def download_rdf_file(url, destination):
    """Gets an RDF file from an URL and stores in a destination
    Keyword arguments:
    url -- The url of the file to download
    destination -- The path to store the downloaded file
    """
    #get the file from Internet
    tempFile = urllib2.urlopen(url)
    parts = []
    #split the URL(we want to get the last part(file name))
    for part in url.split('/'):
        parts.append(part)
    
    #check if the url is an RDF file, if not throw an exception
    if parts[len(parts)-1] == '' or not parts[len(parts)-1].endswith('.rdf'):
        raise Exception, "The url has to point to an rdf file"
    else:
        #add to the destination the last part of the splitted url (length -1)
        destination += parts[len(parts)-1]
        #open the destination file (with wb flags) and writes the "buffer"
        output = open(destination, 'wb')
        output.write(tempFile.read())

    #close the opened file
    output.close()
#####################################################################################
def store_RDF(rdfPath):
    """Stores an RDF file (path or URL) in the Database
    Keyword arguments:
    rdfPath -- the RDF file path, could be a System path or a URL
    """
    configString = 'rdfstore.sqlite'

    store = plugin.get('SQLite', Store)('rdfstore.sqlite')

    #open the DB, if exists doesn't create, if exists, it creates a new one
    store.open(configString, create=True)

    graph = Graph(store)
    #Parse the path to the RDF
    graph.parse(rdfPath)
    #Commit the changes(insert, delete and modifications in to the database)
    graph.commit()

    print("[OK] RDF stored in Database")
    graph.close()
#####################################################################################
def store_ontology(rdfPath):
    """Stores an ontology (RDF) file (path or URL) in the Database
    Keyword arguments:
    rdfPath -- the RDF file path, could be a System path or a URL
    """
    configString = 'rdfstore.sqlite'

    store = plugin.get('SQLite', Store)('rdfstore.sqlite')

    #open the DB, if exists doesn't create, if exists, it creates a new one
    store.open(configString, create=True)

    graph = Graph(store)
    #Parse the path to the RDF
    graph.parse(rdfPath)
    #Commit the changes(insert, delete and modifications in to the database)
    graph.commit()

    print("[OK] Ontology stored in Database")
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
def sparql_query(query):
    """ Makes a sparql query to the SQLite database and returns a result
    Keyword arguments:
    query -- the query to execute

    Returns a result (rdflib result)
    TODO: Return a good formated string and not a raw result
    """	
    prefixes = {}
    #connect to database
    store = plugin.get('SQLite', Store)('rdfstore.sqlite')
    store.open('rdfstore.sqlite', create=True)

    #load the graph
    g = ConjunctiveGraph(store)

    #register the sparql and SQLite plugin for the queries
    plugin.register('SQLite', Store, 'rdflib.store.SQLite', 'SQLite')
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

    return qres
