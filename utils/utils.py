import rdflib
from rdflib import plugin
from rdflib.store import Store
from rdflib import Namespace
from rdflib import Literal
from rdflib import URIRef
from rdflib.store import SQLite
from rdflib.store import Store, NO_STORE, VALID_STORE
from rdflib.graph import *
from rdflib.namespace import Namespace
from rdflib.query import *
from rdflib import sparql
from rdflib.query.result import QueryResult


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
"""def sparql_query(query):

	store = plugin.get('SQLite', Store)('rdfstore.sqlite')
	store.open('rdfstore.sqlite', create=True)
	g = ConjunctiveGraph(store)

	plugin.register('SQLite', Store, 'rdflib.store.SQLite', 'SQLite')

	plugin.register('sparql', sparql.Processor,
		 'rdflib.sparql.bison.Processor', 'Processor')
	plugin.register('SPARQLQueryResult', QueryResult,
	  'rdflib.sparql.QueryResult', 'SPARQLQueryResult')
	qres = g.query(query)

	for row in qres.result:
	  print "%s knows %s" % row" """
