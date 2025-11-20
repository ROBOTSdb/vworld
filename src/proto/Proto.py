from typing import Any
from ProtoAttribute import ProtoAttributes

class Proto:
    defined=False
    name:str="general"
    properties:dict[str,ProtoAttributes]={}
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
    def __setitem__(self,key:str,value:Any)->None:
        if type(key)!=str:
            if self.NoneForEror==True:
                return None
            else:
                raise(ValueError("use string key"))
        self.properties[key]=value
    def __iter__(self):
        return self.properties.__iter__()
    def proto(self,tabs:int=1) -> str:
        value:str=""
        for i in self.properties:
            value+=self.properties[i].proto(tabs=2)
        return value
P=Proto()
P['head']=ProtoAttributes(size=[1,2,3],color="red")
print(P.proto())