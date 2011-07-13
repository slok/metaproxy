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

import urllib2

#import Redland
import RDF
import Redland

# Import graphviz
import sys
sys.path.append('/usr/lib64/graphviz/python/')
import gv

# Import pygraph
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search
from pygraph.readwrite.dot import write

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
def parse_link(link, parserType='rdfxml'):
    """parses a link and returns stream statements
        link to the file
        parser type: rdfxml, ntriples, turtle, trig, guess, rss-tag-soup, rdfa, nquads, grddl
    """
    parser = RDF.Parser(name=parserType)
    return parser.parse_as_stream(link)
####################################################################################
def parse_string(rdfStr, uri, parserType='rdfxml'):
    """parses a string and returns stream statements
        rdfStr: rdf string
        parser type: rdfxml, ntriples, turtle, trig, guess, rss-tag-soup, rdfa, nquads, grddl
    """
    parser = RDF.Parser(name=parserType)
    return parser.parse_string_as_stream(rdfStr, uri)
######################################################################################
def serialize_stream(stream, serializerType='rdfxml'):
    """changes the format(serialize) from stream object(Redland) to a format
        returns a string
        link to the file
        serializer type: rdfxml, rdfxml-abbrev, turtle, ntriples, rss-1.0, dot, html, json, atom, nquads
    """
    ser = RDF.Serializer(name=serializerType)
    return ser.serialize_stream_to_string(stream)
#######################################################################################
def str_to_graph_file(rdfString, uri, storePath, fileType='png'):
    stre = parse_string(rdfString, uri)
    dotSer = serialize_stream(stre, 'dot')

    gvv = gv.readstring(dotSer)
    gv.layout(gvv,'dot')
    gv.render(gvv,fileType,storePath)
#######################################################################################
def rdf_to_graph_file(rdfLink, storePath, fileType='png'):
    stre = parse_link(rdfLink)
    dotSer = serialize_stream(stre, 'dot')

    gvv = gv.readstring(dotSer)
    gv.layout(gvv,'dot')
    gv.render(gvv,fileType,storePath)
#######################################################################################
def rdf_to_graph_str(rdfLink):
    stre = parse_link(rdfLink)
    dotSer = serialize_stream(stre, 'dot')

    gvv = gv.readstring(dotSer)
    gv.layout(gvv,'dot')
    graphStr = gv.renderdata(gvv,'svg')
    return graphStr

