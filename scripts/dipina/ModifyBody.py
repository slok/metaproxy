import abc
import urllib2
from utils.utils import debug_print
from scripts.ModifyBodyBase import ModifyBodyBase

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
                        </ul>
                        <div id="fragment-1">"""
        midHTML= """
                    </div>
                        <div id="fragment-2">
                        
                        <pre class="brush: xhtml">
                        """
                        
        syntaxHigh=     """
                        
                        </pre>
                        
                        <script type="text/javascript">SyntaxHighlighter.all()</script>
                        
                        """
                        
        finHTML="""                   
                        </div>
                    </div>
                </body>
            </html>
                 """
        
        tempFile = urllib2.urlopen('http://paginaspersonales.deusto.es/dipina/resources/diego.rdf')

        return initHTML + posBody + midHTML + tempFile.read() + syntaxHigh + finHTML
