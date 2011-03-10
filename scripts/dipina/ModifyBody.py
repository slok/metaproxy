import abc
import urllib2
from utils.utils import debug_print
from scripts.ModifyBodyBase import ModifyBodyBase
from django.conf import settings
from BeautifulSoup import BeautifulSoup          # For processing HTML
from BeautifulSoup import BeautifulStoneSoup     # For processing XML
from BeautifulSoup import SoupStrainer
from BeautifulSoup import Tag
from BeautifulSoup import NavigableString


class ModifyBody(ModifyBodyBase):
    
    def body_modification_logic(self, body):
        
        head = self.get_Head_and_insert_js(body)
        bodyHtml = self.get_body_html(body)
                 
        body = head + bodyHtml
        return body

    def get_Head_and_insert_js(self, body):
        print "####[getting head]####"
        #Insert the scripts for the tabs in head 
        posHead = body.find("</head>") - 1
        jQScript = """
                    <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css" rel="stylesheet" type="text/css"/>
                    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script>
                    <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js"></script>
                    
                    <script>
                        $(document).ready(function() {
                            $("#tabs").tabs();
                        });
                    </script>
                    
                    <link href="/static/css/shCore.css" rel="stylesheet" type="text/css" />
                    <link href="/static/css/shThemeRDark.css" rel="stylesheet" type="text/css" />
                    <script type="text/javascript" src="/static/js/shCore.js"></script>
                    <script type="text/javascript" src="/static/js/shBrushXml.js"></script>
                   """
        bodyAux = body[:posHead] + jQScript + body[(posHead):]
        
        head =  bodyAux[bodyAux.find("<head>"): bodyAux.find("</head>") + 7]
        
        return head
    
    def get_body_html(self, body):
        posBody = body[(body.find("<body>") + 6): body.find("</body>")]
        
        initHTML= """
                  <body>
                    <div id="tabs">
                        <ul>
                            <li><a href="#fragment-1"><span>WebPage</span></a></li>
                            <li><a href="#fragment-2"><span>XML FOAF</span></a></li>
                            <li><a href="#fragment-3"><span>GRDDL Parsing</span></a></li>
                            <li><a href="#fragment-4"><span>Web Scrapping(Awards)</span></a></li>
                        </ul>
                        <div id="fragment-1">"""
        frag2= """
                        </div>
                        <div id="fragment-2">
                    """       
                        
        frag3="""                   
                        </div>
                        <div id="fragment-3">
                    """
        frag4="""
                        </div>
                        <div id="fragment-4">
                    """
        finHTML="""
                    </div>
                </body>
            </html>
                 """
        syntaxHigh='<script type="text/javascript">SyntaxHighlighter.all()</script>'
        links = self.getAllRdfLinks(body)
        rdfs = self.addRDFsCodeInHTMLLinks(links)
        awardXML = self.createAwardXML(body)
        awardXML = self.addRDFsCodeInHTMLStr(awardXML)
        return initHTML + posBody + frag2 + rdfs + frag3 + 'VOID'+ frag4+ awardXML +syntaxHigh + finHTML

    def addRDFsCodeInHTMLLinks(self, linkList):
        finalHtml=''
        preStart = '<pre class="brush: xhtml">'
        preEnd = '</pre>'
        for i in linkList:
            tempFile = urllib2.urlopen(i)
            finalHtml = finalHtml + '-------------------' +preStart +  tempFile.read()  +preEnd 
        
        
        return finalHtml
    
    def addRDFsCodeInHTMLStr(self, xml):
        
        finalHtml = '<pre class="brush: xhtml">\n' + xml + '\n</pre>'
    
        return finalHtml
    
    def getAllRdfLinks(self, body):
        links = []
        linkList = []
        #get all links
        for link in BeautifulSoup(body, parseOnlyThese=SoupStrainer('a')):
            #get only links and .rdf ones [[[[[[[[[[[[[(POC .vcf too)]]]]]]]]]]]]]]]] delete .vcf
            if link.has_key('href') and ('.rdf' in link['href'] or '.vcf' in link['href']):
                links.append(link['href'])
        
        #add prefix to the url
        for i in links:
            debug_print(settings.REVPROXY_SETTINGS[0][1])
            linkList.append(settings.REVPROXY_SETTINGS[0][1] + i)
        
        return linkList
    
    def createAwardXML(self, body):
        #get all the blocks of wards
        htmlSoup = BeautifulSoup(body, parseOnlyThese=SoupStrainer('dd'))
        #get all the titles of the awrads
        htmlTitles = BeautifulSoup(body, parseOnlyThese=SoupStrainer('dt'))
        awardCont = 0
        
        #create RDF and properties
        xmlSoup = BeautifulStoneSoup()
        rdfRDF = Tag(xmlSoup, 'rdf:RDF',[('xmlns:rdf','http://www.w3.org/1999/02/22-rdf-syntax-ns#')
                                    ,('xmlns:dc', 'http://purl.org/dc/elements/1.1/') ])
        
        #add to the xml first property
        xmlSoup.append(rdfRDF)
        for award in htmlSoup: #get "dd" blocks (each is an award)
            
            dcDate = Tag(xmlSoup, 'dc:date')
            dcContrib =  Tag(xmlSoup, 'dc:contributor')
            dcCreator =  Tag(xmlSoup, 'dc:creator')
            dcRelation =  Tag(xmlSoup, 'dc:relation')
            
            #add titles to rdf description
            rdfDesc = Tag(xmlSoup, 'rdf:Description', [('dc:title', htmlTitles.contents[awardCont].contents[0])])
            rdfRDF.append(rdfDesc)
            #increment the titles counter
            awardCont = awardCont + 1
            
            for awardProp in award.contents: #get each div block (content of dd)
                try:
                    for props in awardProp.contents: #get each property
                        try:
                            print props.contents[0].contents[0]
                            if len(props.contents) == 2:
                                if props.contents[0].contents[0] == 'Date' or  props.contents[0].contents[0] == 'date':
                                    rdfDesc.append(dcDate)
                                    dcDate.insert(0, NavigableString(props.contents[1]))
                                elif props.contents[0].contents[0] == 'Entity' or  props.contents[0].contents[0] == 'entity': #error in Alava enprender link
                                     rdfDesc.append(dcContrib)
                                     dcContrib.insert(0, NavigableString(props.contents[1]))
                                elif props.contents[0].contents[0] == 'Author' or  props.contents[0].contents[0] == 'author' or \
                                    props.contents[0].contents[0] == 'Authors' or  props.contents[0].contents[0] == 'authors': 
                                     rdfDesc.append(dcCreator)
                                     dcCreator.insert(0, NavigableString(props.contents[1]))
                                elif props.contents[0].contents[0] == 'Role' or  props.contents[0].contents[0] == 'role': 
                                     rdfDesc.append(dcRelation)
                                     dcRelation.insert(0, NavigableString(props.contents[1])) 
                                """if props.contents[0].contents[0] == 'Title' or props.contents[0].contents[0] == 'title':
                                    rdfDesc = Tag(xmlSoup, 'rdf:Description', [('dc:title', props.contents[1])])
                                    rdfRDF.append(rdfDesc)
                                else:"""
                        except:
                            pass
                except:
                    pass

        return xmlSoup.prettify()
