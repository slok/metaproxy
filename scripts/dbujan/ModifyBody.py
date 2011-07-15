import abc
import urllib2
import re
from utils.utils import debug_print
from utils.rdf import rdf_to_graph_file
from scripts.ModifyBodyBase import ModifyBodyBase

from django.conf import settings

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
        
        debug_print(self.headers)
        
        #we will work with utf8
        self.body = unicode(self.body, "utf-8", errors='replace')
        
        newBody = self._change_Css()
        headHtml = self._get_Head_and_insert_Css(newBody)
        bodyHtml = self._get_body_html(newBody)
                 
        self.body =  headHtml + bodyHtml
        
    def _change_Css(self):
        
        body = self.body
        
        newCss = "/static/css/bujan.css"
        
        regularExpressionIn = '\w+\.css'
        reg = re.compile(regularExpressionIn)

        m = reg.search(body)
        
        changedHtml =  body[:m.start(0)] + newCss + body[m.end(0):]
        
        return changedHtml
        
    def _get_Head_and_insert_Css(self, body):
        
        print "####[getting head]####"
        posHead = body.find("</head>") - 1
        webCss= '<link href="/static/css/proxiedWeb.css" rel="stylesheet" type="text/css" />'
        bodyAux = body[:posHead] + webCss + body[posHead:]
        
        head =  bodyAux[: bodyAux.find("</head>") + 7]
        
        #convert result to unicode(if they are unicode already exception will be catch and wouldn't be done nothing)
        try:
            head = unicode(head, "utf-8", errors='replace')
        except:
            pass
        
        return head
    
    def _get_body_html(self, body):
        
        regularExpressionIn = '<body[\w"= ]*>'
        reg = re.compile(regularExpressionIn)

        m = reg.search(body)
        
        homeButton = '\n<div id="homeLink"><a href="/"><img id="homeButton" src="/static/img/home.png" alt="Return Home"/></a></div>'
               
        bodyTagSize = m.group(0)
        
        
        finalHtml = body[m.start(0):m.end(0)] + homeButton + body[m.end(0):]
        
        return finalHtml
