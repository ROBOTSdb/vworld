from typing import Any
from .ProtoAttribute import ProtoAttributes

class Proto:
    properties:dict[str,ProtoAttributes]
    NoneForEror:bool=True
    def __getitem__(self,key:str)->Any:
        if type(key)!=str:
            if self.NoneForEror==True:
                return None
            else:
                raise(ValueError("use string key"))
        if key in self.properties:
            return self.properties[key]
        else:
            if self.NoneForEror:
                return None
            else:
                raise(KeyError("key not found"))
    def __iter__(self):
        return self.properties.__iter__()