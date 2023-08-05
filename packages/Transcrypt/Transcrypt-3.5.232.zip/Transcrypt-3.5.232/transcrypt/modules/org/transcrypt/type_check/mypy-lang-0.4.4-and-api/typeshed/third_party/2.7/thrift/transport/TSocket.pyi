# Stubs for thrift.transport.TSocket (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

from .TTransport import *

class TSocketBase(TTransportBase):
    handle = ... # type: Any
    def close(self): ...

class TSocket(TSocketBase):
    host = ... # type: Any
    port = ... # type: Any
    handle = ... # type: Any
    def __init__(self, host=..., port=..., unix_socket=..., socket_family=...) -> None: ...
    def setHandle(self, h): ...
    def isOpen(self): ...
    def setTimeout(self, ms): ...
    def open(self): ...
    def read(self, sz): ...
    def write(self, buff): ...
    def flush(self): ...

class TServerSocket(TSocketBase, TServerTransportBase):
    host = ... # type: Any
    port = ... # type: Any
    handle = ... # type: Any
    def __init__(self, host=..., port=..., unix_socket=..., socket_family=...) -> None: ...
    def listen(self): ...
    def accept(self): ...
