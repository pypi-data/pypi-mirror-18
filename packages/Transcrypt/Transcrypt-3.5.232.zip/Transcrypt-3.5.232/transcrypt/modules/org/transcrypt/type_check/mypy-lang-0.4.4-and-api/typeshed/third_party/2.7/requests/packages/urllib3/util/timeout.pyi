# Stubs for requests.packages.urllib3.util.timeout (Python 3.4)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any
from .. import exceptions

TimeoutStateError = exceptions.TimeoutStateError

def current_time(): ...

class Timeout:
    DEFAULT_TIMEOUT = ...  # type: Any
    total = ...  # type: Any
    def __init__(self, total=..., connect=..., read=...) -> None: ...
    @classmethod
    def from_float(cls, timeout): ...
    def clone(self): ...
    def start_connect(self): ...
    def get_connect_duration(self): ...
    @property
    def connect_timeout(self): ...
    @property
    def read_timeout(self): ...
