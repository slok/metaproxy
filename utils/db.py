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

import RDF
import Redland
import MySQLdb 


def create_mysql_db(user, password, db):
    """
        Creates a mysql database
    """
    connDb=MySQLdb.connect(host="localhost", user=user, passwd=password)
    c=connDb.cursor()
    c.execute('CREATE DATABASE ' + db)
    print("[" + db +" DATABASE CREATED ]")
#####################################################################################
def connect_librdf_mysql(user, password, db):
    """
        Connects Redland(libRDF) and mysql
        returns Storage instance
    """
    options = ''
    #options += 'contexts=\'yes\', '
    options += 'write=\'false\', '
    options += 'host=\'localhost\', '
    options += 'database=\'' + db + '\', '
    options += 'user=\'' + user + '\', '
    options += 'password=\'' + password + '\''

    try:
        storage=RDF.Storage(storage_name="mysql",
                    name=db,
                    options_string=options)
    except:
        create_mysql_db(user, password, db)
        # if the new = true is always on, then the 'new' ruins the stored data every time we connect
        # (but the data continues in the datasabase, stored) is a weird "issue", so we only put the 
        # flag to true, the first time that the database needs to be created otherwise the queries always are "Null"
        options += ', new=\'true\''
        
        storage=RDF.Storage(storage_name="mysql",
                    name=db,
                    options_string=options)
    print("[ CONNETED TO "+ db +" DATABASE ]")
    return storage
#####################################################################################
def store_RDF(rdfPath, user, password, db):
    """Stores an RDF file (path or URL) in the Database
    Keyword arguments:
    rdfPath -- the RDF file path, could be a System path or a URL
    user -- The user for accesing the DB
    password -- The password of the user for accesing the DB
    db -- The DB that we are going to access
    """
    st= connect_librdf_mysql(user, password, db)
        
    model=RDF.Model(st)
    
    if not (rdfPath.startswith('http://') or rdfPath.startswith('HTTP://')):
        rdfPath = 'file:' + rdfPath
        
    #Redland.librdf_model_transaction_start(model._model)
    try:
        # Do something
        parser=RDF.Parser(name="rdfxml",mime_type="application/rdf+xml")
        parser.parse_into_model(model, rdfPath)
        #Redland.librdf_model_transaction_commit(model._model)
        #model.sync()
    except:
        pass
        #Redland.librdf_model_transaction_rollback(model._model)

    print("["+ rdfPath +" RDF STORED ]")
    #Redland.librdf_free_storage(st._storage);

#####################################################################################
def sparql_query(query, user, password, db, output=None):
    """ Makes a sparql query to the SQLite database and returns a result
    Keyword arguments:
    query -- the query to execute
    user -- The user for accesing the DB
    password -- The password of the user for accesing the DB
    db -- The DB that we are going to access
    output -- the output type could be xml only, for now, so The is no parameter
    
    Returns a result (rdflib result)
    """	
    st= connect_librdf_mysql(user, password, db)
    
    model=RDF.Model(st)

    q1 = RDF.Query(query ,query_language='sparql')
    q1Result = q1.execute(model) 
    #q1Result = model.execute(q1) 
    
    print("[ SPARQL QUERY DONE ]")
    #Redland.librdf_free_storage(st._storage);
    
    #return in str(XML)
    return q1Result.to_string()
