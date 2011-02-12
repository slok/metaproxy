import abc

class ModifyBodyBase(object):
    __Metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def body_modification_logic(self, body):
        """Gets the boy from an HTML request and applys any logic to
        modify, after the method returns the modified body"""
        raise NotImplementedError
        return
