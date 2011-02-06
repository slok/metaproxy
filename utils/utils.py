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