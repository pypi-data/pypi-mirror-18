# Stubs for yaml.serializer (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any
from yaml.error import YAMLError

class SerializerError(YAMLError): ...

class Serializer:
    ANCHOR_TEMPLATE = ... # type: Any
    use_encoding = ... # type: Any
    use_explicit_start = ... # type: Any
    use_explicit_end = ... # type: Any
    use_version = ... # type: Any
    use_tags = ... # type: Any
    serialized_nodes = ... # type: Any
    anchors = ... # type: Any
    last_anchor_id = ... # type: Any
    closed = ... # type: Any
    def __init__(self, encoding=..., explicit_start=..., explicit_end=..., version=..., tags=...) -> None: ...
    def open(self): ...
    def close(self): ...
    def serialize(self, node): ...
    def anchor_node(self, node): ...
    def generate_anchor(self, node): ...
    def serialize_node(self, node, parent, index): ...
