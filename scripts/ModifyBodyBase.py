import abc

class ModifyBodyBase(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def __init__(self, body, headers, proxied_url):
        return
    
    @abc.abstractmethod
    def body_modification_logic(self):
        """Gets the boy from an HTML request and applys any logic to
        modify, after the method returns the modified body"""
        return

    @abc.abstractproperty
    def body(self):
        return 'body: nothing to see here, move along...'
    
    @body.setter
    def body(self, newBody):
        return
    
    @abc.abstractproperty
    def headers(self):
        return 'headers: nothing to see here, move along...'
    
    @headers.setter
    def headers(self, newHeaders):
        return
    
    @abc.abstractproperty
    def proxied_url(self):
        return 'proxied_url: nothing to see here, move along...'
    
    @proxied_url.setter
    def proxied_url(self, newProxied_url):
        return
    
