import abc
import urllib2
import re
import RDF
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
        initializeTweet =   """
                            <script language="javascript" 
                                src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" 
                                type="text/javascript">
                            </script>
                            <script language="javascript" 
                                src="http://tweet.seaofclouds.com/jquery.tweet.js" 
                                type="text/javascript">
                            </script> 
                        """
        
        tweetJsFunc =   """
                            <script type='text/javascript'>
                                $(document).ready(function(){
                                    $(".tweet").tweet({
                                        username: ["sharem", "slok69"],
                                        avatar_size: 32,
                                        count: 5,
                                        loading_text: "loading tweets..."
                                    });
                                });
                            </script> 
                        """
        tweetCss = '<link href="http://tweet.seaofclouds.com/jquery.tweet.css" media="all" rel="stylesheet" type="text/css"/> '
        homeCss = '<link href="/static/css/proxiedWeb.css" rel="stylesheet" type="text/css" />'
        #Search and create the new head
        pattHeadFinish = '</head>'
        regexHeadFinish = re.search(pattHeadFinish, self.body)
        
        bodyAux = self.body[:regexHeadFinish.start(0)] + initializeTweet + tweetJsFunc + tweetCss + homeCss + self.body[regexHeadFinish.start(0):]
        
        self.body = bodyAux
    
    def _modify_HTML_body(self):
        
        homeButton = '<div id="homeLink"><a href="/"><img id="homeButton" src="/static/img/home.png" alt="Return Home"/></a></div>'
        #tweetPlace = '<div class="tweet"></div> '
        tweetPlace = '<center> <div class="tweet" style="width:400px; text-align:left"></div> </center>'
        
        #place the home button
        pattBodyStart  = '<body[\w"= ]*>'
        regexBodyStart = re.search(pattBodyStart, self.body)
        self.body =  self.body[:regexBodyStart.end(0)+1] + homeButton + self.body[regexBodyStart.end(0)+1:]
        
        #place the twitter plugin at the bottom
        pattBodyFinish = '</body>'
        regexBodyFinish = re.search(pattBodyFinish, self.body)
        
        bodyAux = self.body[:regexBodyFinish.start(0)] + tweetPlace + self.body[regexBodyFinish.start(0):]
        self.body = bodyAux 
