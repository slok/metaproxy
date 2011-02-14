import abc
from scripts.ModifyBodyBase import ModifyBodyBase

class ModifyBody(ModifyBodyBase):
    
    def body_modification_logic(self, body):
        
        body = body.replace('Diego', 'Iraide') 
        return body

