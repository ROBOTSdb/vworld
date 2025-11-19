from .proto import Proto
class Session:
    protos:list[Proto]=[]
    def add_proto(self,proto:Proto):
        ...
class LiveSession:
    ...
