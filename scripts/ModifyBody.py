import abc
import urllib2
import re
import RDF
from utils import rdf
from scripts.ModifyBodyBase import ModifyBodyBase
from django.conf import settings
import BeautifulSoup    


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
                
        #we will work with utf8
        self.body = unicode(self.body, "utf-8", errors='replace')
        
        #HTML Head block modification
        self._modify_HTML_head()
        
        #HTML Body block modification
        self._modify_HTML_body()
                 

    def _modify_HTML_head(self):
        """
            Gets the head html block of the HTML and applys all the needed modifications
            for example add css, javascripts... then saves in the attribute body
        """
        
        #Code that we will insert in the head
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
        
        #regular expressions for searching the head block, insert data and then save in the class attribute
        #pattHeadStart = '<head[\w"=\/\:\.\- ]*>'
        pattHeadFinish = '</head>'
    
        #regexHeadStart = re.search(pattHeadStart, body)
        regexHeadFinish = re.search(pattHeadFinish, self.body)
        
        bodyAux = self.body[:regexHeadFinish.start(0)] + jQScript + self.body[regexHeadFinish.start(0):]
        
        self.body = bodyAux
        #convert result to unicode(if they are unicode already exception will be catch and wouldn't be done nothing)
        """try:
            head = unicode(head, "utf-8", errors='replace')
        except:
            pass
        """
    
    def _modify_HTML_body(self):
        
        pattBodyStart  = '<body[\w"= ]*>'
        pattBodyFinish = '</body>'
        regexBodyStart = re.search(pattBodyStart, self.body)
        regexBodyFinish = re.search(pattBodyFinish, self.body)
        
        mainPageBody = self.body[regexBodyStart.end(0): regexBodyFinish.start(0)]

        #Tab creation (All, XML and GRDDL, the contentn of the tab and the declaration)
        #tab variable is a tuple with the declarations [0] and the content of the tabs [1]
        tabs = self._createTabs()

        #add the declaration of the tabs
        initHTML= """
                    <div id="homeLink"><a href="/"><img id="homeButton" src="/static/img/home.png" alt="Return Home"/></a></div>
                    <div id="tabs">
                        <ul>"""+ tabs[0] +"""
                        </ul>
                        <div id="fragment-web">"""
        endMainTab=  """
                        </div>
                            """       
        finHTML="""
                        <script type="text/javascript">SyntaxHighlighter.all()</script>
                    </div>
                 """
        #Last string creation (now we are goint to use the tab content)      
        stringsForHTML = [initHTML, mainPageBody, endMainTab, tabs[1], finHTML]
        final = ''
        
        #convert all to unicode(if they are unicode already exception will be catch and wouldn't be done nothing)
        for string in  stringsForHTML:
            try:
                string = unicode(string, "utf-8", errors='replace')
            except:
                pass
            final = final + string
        
        self.body = self.body[: regexBodyStart.end(0)] + final + self.body[regexBodyFinish.start(0):]
        
    def _createTabs(self):
        """
            This method 'creates' alll the tabs, technically, this method does all the calls
            for all the neccesary tabs(RDF/GRDDL), then returns a tuple with two vars, the 
            first position of the tuple are the declarations of the tabs, and the second position 
            are the contents of all the declared tabs. They are separate because the jquery plugin
            need first to declare, and then when all the tabs are declared, put the content
        """
        
        #tab necessary data
        mainTab = '\n<li><a href="#fragment-web"><span>WebPage</span></a></li>'
        tabs = mainTab
        tabContent=''
        cont = 0
        
        links = self._getAllRdfLinks()
        #Declare XML/RDF TABS and create content
        for i in links:
            #split the url to get the final name
            tmp = i.split('/')
            name = tmp[len(tmp)-1]  #get the last array postion (the name of the file, ex: foaf.rdf)
            name = name.split('.') 
            finalName = name[0]     #get the las array position (the name of file without extension, ex: foaf)
            finalNamePar = finalName + '(RDF/XML)'
            #create the HTML code for the tab declaration
            tabs = tabs + '\n<li><a href=\"#fragment-'+ finalName +'\"><span>' + finalNamePar + '</span></a></li>'
            
            #create RDF tab
            downloadedXml = urllib2.urlopen(i).read() #get RDF content
            try:
                #if we want to print there is the need to change errors to 'ignore'
                downloadedXml = unicode(downloadedXml, "utf-8", errors='replace')
            except:
                pass
            #and create the whole content tab
            tabContent += self._createSingleXMLGraphTab(downloadedXml, finalName, i, cont)   
            cont += 1 
        
        #Declare GRDDL TAB and create content (if there is in the html...)
        if self._checkGRDDL():
            tabs = tabs + '\n<li><a href=\"#fragment-grddl\"><span>GRDDL Parsing</span></a></li>'
            tabContent += self._createSingleXMLGraphTab(self._parseGRDDL(),'grddl', None, cont)
            cont +=1
        
        #return a tuple with: (tab declarations, tab contents) 
        return (tabs, tabContent) 
    
    def _createSingleXMLGraphTab(self, contentStr, key, url, cont):
        """
            Creates a single tab that is XML and Graph type, like the RDFs or the GRDDLs,
            this tabs consist in an XML String and graph representation of that XML. 
            receives: the content of the tab(the XML string), and the key(is the title of the tab),
            the url of the XML file, and the counter of the tab(this is for the iviewer)
        """
        preStart = """
                    <div id = "code">
                        <div id="codeBox">
                            <pre class="brush: xhtml">\n
                   """
        preEnd = """
                            \n</pre>
                        </div>
                    </div>
                    
                    <script>
                    $(document).ready(function() {
                    var iviewer = {};
                    $("#graphViewer"""+str(cont+1)+"""\").iviewer(
                  {
                """
        end= """
                      initCallback: function()
                      {
                        iviewer = this;
                      }
                    });
                    });
                    </script>
                    
                    <div class="wrapper">
                        <div id="graphViewer"""+str(cont+1)+"""\" class="viewer" ></div>
                        <br />
                    </div>
                </div>
                 """
        
        #add the tab block head(ex: <div id="fragment-grddl">)
        tmp = '<div id=\"fragment-'+ key +'\">'
        
        #GRAPH TIME!!
        #create the destination for saving the SVG graph      
        graphDest = 'static/tmp/'+str(key)+'.svg'
        
        #In GRDDL we have the exception that the graph is made with an string and not with an URL
        if url == None:
            rdf.str_to_graph_file(contentStr, self.proxied_url, graphDest, 'svg') #the url is this (actual url)
        else:
            rdf.rdf_to_graph_file(url, graphDest, 'svg')
        
        #We retrieve the dir of the src image to show it in the viewer 
        imgSource=' src: "/'+graphDest+'",'
        
        #assemble the final tab code, now we have a awesome complete tab. ta-da!! :D
        code = tmp + preStart + contentStr + preEnd + imgSource + end
        return code
        
    
    def _getAllRdfLinks(self):
        """
        Get all the RDF links that are in the HTML and return the links in a list
        """
        body = self.body
        links = []
        linkList = []
        
        #rdfHtmlRegex = '\.(html|rdf)' 
        localRdfRegex = '^(?!http).*\.rdf$'
        rdfMatch = re.compile(localRdfRegex)
        
        #get all links
        for link in BeautifulSoup.BeautifulSoup(body, parseOnlyThese=BeautifulSoup.SoupStrainer('a')):
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
        only http://... .So the aim of this method is avoid the bad made urls and not
        get http://.../index.html/resources/foaf.rdf. We only want the root url ;)
        """
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
            return unicode(rdf.serialize_stream(stream), "utf-8", errors='replace')
        else:
            #return None
            return 'No GRDDL in this html....'
