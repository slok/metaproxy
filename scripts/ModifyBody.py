import abc
import urllib2
import re
import RDF

#from utils.utils import debug_print
#from utils.utils import rdf_to_graph_file
from utils import utils
from scripts.ModifyBodyBase import ModifyBodyBase

from django.conf import settings

from BeautifulSoup import BeautifulSoup          # For processing HTML
from BeautifulSoup import BeautifulStoneSoup     # For processing XML
from BeautifulSoup import SoupStrainer
from BeautifulSoup import Tag
from BeautifulSoup import NavigableString


class ModifyBody(ModifyBodyBase):
    
    def __init__(self, body, headers, proxied_url):
        self.body = body
        self.headers = headers
        self.proxied_url = proxied_url
    
    @property
    def proxied_url(self):
        return self._proxied_url
    
    @proxied_url.setter
    def proxied_url(self, newProxied_url):
        self._proxied_url = newProxied_url
    
    @property
    def body(self):
        return self._body
    
    @body.setter
    def body(self, newBody):
        self._body = newBody
    
    @property
    def headers(self):
        return self._headers
    
    @headers.setter
    def headers(self, newHeaders):
        self._headers = newHeaders
    
    def body_modification_logic(self):
        
        utils.debug_print(self.headers)
        
        #we will work with utf8
        self.body = unicode(self.body, "utf-8", errors='replace')
        
        head = self._get_Head_and_insert_js()
        bodyHtml = self._get_body_html()
                 
        self.body = head + bodyHtml

    def _get_Head_and_insert_js(self):
        
        body = self.body
        print "####[getting head]####"
        #Insert the scripts for the tabs in head 
        posHead = body.find("</head>") - 1
        jQScript = """
                    <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css" rel="stylesheet" type="text/css"/>
                    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script>
                    <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js"></script>
                    <link href="/static/css/proxiedWeb.css" rel="stylesheet" type="text/css" />
                    
                    <script>
                        $(document).ready(function() {
                            $("#tabs").tabs();
                            $("#viewer").iviewer({
                               update_on_resize: true,
                               initCallback: function ()
                               {
                                   var object = this;
                                   object.fit();
                                   $("#in").click(function(){ object.zoom_by(1);}); 
                                   $("#out").click(function(){ object.zoom_by(-1);}); 
                                   $("#fit").click(function(){ object.fit();}); 
                                   $("#orig").click(function(){  object.set_zoom(100); }); 
                                   $("#update").click(function(){ object.update_container_info();});
                               },
                               onMouseMove: function(object, coords) { },
                               onStartDrag: function(object, coords) { },
                               onDrag: function(object, coords) { }
                            });
                        });
                    </script>
                    
                    <link href="/static/css/shCore.css" rel="stylesheet" type="text/css" />
                    <link href="/static/css/shThemeRDark.css" rel="stylesheet" type="text/css" />
                    <script type="text/javascript" src="/static/js/shCore.js"></script>
                    <script type="text/javascript" src="/static/js/shBrushXml.js"></script>
                    
                    <script type="text/javascript" src="/static/js/jquery.iviewer.js"></script>
                    <script type="text/javascript" src="/static/js/jquery.mousewheel.min.js"></script>
                    <link href="/static/css/jquery.iviewer.css" rel="stylesheet" type="text/css" />

                   """
        regularExpressionIn = '<head[\w"=\/\:\.\- ]*>'
        reg = re.compile(regularExpressionIn)
        m = reg.search(body)
        
        bodyAux = body[:posHead] + jQScript + body[(posHead):]
        
        head =  bodyAux[m.start(0): bodyAux.find("</head>") + 7]
        
        #convert result to unicode(if they are unicode already exception will be catch and wouldn't be done nothing)
        try:
            head = unicode(head, "utf-8", errors='replace')
        except:
            pass
        
        return head
    
    def _get_body_html(self):
        body = self.body
        
        posBody = body[(body.find("<body>") + 6): body.find("</body>")]
        #get data
        syntaxHigh='<script type="text/javascript">SyntaxHighlighter.all()</script>'
        
        #tab necessary data
        rdfNameAndUrl={}
        tabs = '<li><a href="#fragment-web"><span>WebPage</span></a></li>'
        links = self._getAllRdfLinks()
        
        for i in links:
            #split the url to get the final name
            tmp = i.split('/')
            name = tmp[len(tmp)-1]
            name = name.split('.')
            finalName = name[0]
            finalNamePar = finalName + '(RDF-XML)'
            #create the HTML code for the tab declaration
            tabs = tabs + '\n<li><a href=\"#fragment-'+ finalName +'\"><span>' + finalNamePar + '</span></a></li>'
            #add to the dict
            rdfNameAndUrl[finalName] = i
            
        #set all the tabs that we want
        #tabs = tabs + '\n<li><a href=\"#fragment-grddl\"><span>GRDDL Parsing</span></a></li>'

        #get all the HTM code fragment from the RDF tabs
        rdfs = self._addRDFsCodeInHTMLLinks(rdfNameAndUrl)

        initHTML= """
                  <body>
                    <div id="homeLink"><a href="/"><img id="homeButton" src="/static/img/home.png" alt="Return Home"/></a></div>
                    <div id="tabs">
                        <ul>"""+ tabs +"""
                        </ul>
                        <div id="fragment-web">"""
        fragRDFs= """
                        </div>
                    """       
        finHTML="""
                    </div>
                </body>
            </html>
                 """
       
        #stringsForHTML = [initHTML, posBody, fragRDFs, rdfs, fragGrddl, 'call to the grddl parser', fragScrap, awardXML, syntaxHigh, finHTML]
        stringsForHTML = [initHTML, posBody, fragRDFs, rdfs, syntaxHigh, finHTML]
        final = ''
        #convert all to unicode(if they are unicode already exception will be catch and wouldn't be done nothing)
        for string in  stringsForHTML:
            try:
                string = unicode(string, "utf-8", errors='replace')
            except:
                pass
            final = final + string
        return final

    def _addRDFsCodeInHTMLLinks(self, linkDict):
        finalHtml=''
        preStart = """
                    <div id = "code">
                        <div id="codeBox">
                            <pre class="brush: xhtml">\n
                   """
        #We need to include the iviewer script in the HTML code of the 
        #page in order to visualize the RDF graph 
        preEnd = """
                            \n</pre>
                        </div>
                    </div>
                    
                    <script>
                    $(document).ready(function() {
                    var iviewer = {};
                    $("#graphViewer").iviewer(
                  {
                """
        
        
        #create a block of tabs(the content)
        for key, val in linkDict.iteritems():
            tempFile = urllib2.urlopen(val).read()
            try:
                #if we want to print there is the need to change errors to 'ignore'
                tempFile = unicode(tempFile, "utf-8", errors='replace')
            except:
                pass
            #add the tab block head 
            tmp = '<div id=\"fragment-'+ key +'\">'
            #create and save the graph (is in the for, because is one grafh for each RDF/XML)        
            graphDest = 'static/tmp/'+str(key)+'.svg'
            
            utils.rdf_to_graph_file(val, graphDest, 'svg')
            
            #We retrieve the dir of the src image to show it in the viewer 
            imgSource=' src: "/'+graphDest+'",'
            
            preEnd2= """
                      initCallback: function()
                      {
                        iviewer = this;
                      }
                    });
                    });
                    </script>
                    
                    <div class="wrapper">
                        <div id="graphViewer" class="viewer" ></div>
                        <br />
                    </div>
                 """
            
            
            #and last but not least add all the parts to create one (html to rule them 
            #all, one html to find them, one html to bring them all and in the darkness bind them)
            finalHtml = finalHtml + tmp +preStart + tempFile + preEnd + imgSource + preEnd2 +'</div>'
        
        #debug_print(finalHtml)
        return finalHtml
    
    def _getAllRdfLinks(self):
        body = self.body
        links = []
        linkList = []
        
        #rdfHtmlRegex = '\.(html|rdf)' 
        localRdfRegex = '^(?!http).*\.rdf$'
        rdfMatch = re.compile(localRdfRegex)
        
        #get all links
        for link in BeautifulSoup(body, parseOnlyThese=SoupStrainer('a')):
            #if is a link and matchs the pattern of a local RDF(Examples: foo.rdf or foo/bar.rdf)
            # and not a link to an RDF(Example: http://www.foo.com/bar.rdf)
            try:
                href = link['href']
                if re.search(rdfMatch, href):
                    links.append(link['href'])
            except:
                pass
        
        #add prefix to the url
        for i in links:
            linkList.append(self._guessBestUrl() + i)
        
        return linkList
        
    def _guessBestUrl(self):
        """We check if at least one of our proxied web urls (in the settings.py 
        of Django root path) is contained in the requested url to proxy, by this
        operation we ensure that we don't get urls like: http://.../index.html and 
        only http://..."""
        for i in settings.REVPROXY_SETTINGS:
            if i[1] in self.proxied_url:
                url = i[1]
                break
        return url
        
    def _checkGRDDL(self):
        """
        Checks if the document(HTML) has GRDDL
        """
        #rel="transformation" href=
        regularExpressionIn = ' +rel *= *" *transformation *" *href *='
        reg = re.compile(regularExpressionIn)
        aux = reg.findall(self.body)
        #if is GRDDL then parse
        if len(aux) > 0:
            return True
        else:
            return False
            
    def _parseGRDDL(self):
        """
        Checks if the document(HTML) has GRDDL and if it has, then parse to 
        extract the RDF in XML format 
        """

        #if is GRDDL then parse
        if self._checkGRDDL():
            parser = RDF.Parser(name='grddl')
            stream = parser.parse_string_as_stream(self.body, self.proxied_url) 
            return utils.serialize_stream(stream)
        else:
            #return None
            return 'No GRDDL in this html....'
