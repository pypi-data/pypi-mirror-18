# Stubs for uuid

from typing import Tuple

Int = __builtins__.int
Bytes = __builtins__.bytes
FieldsType = Tuple[Int, Int, Int, Int, Int, Int]

class UUID:
    def __init__(self, hex: str=..., bytes: Bytes=..., bytes_le: Bytes=..., fields: FieldsType=..., int: Int=..., version: Int=...) -> None: ...

    @property
    def bytes(self) -> Bytes: ...

    @property
    def bytes_le(self) -> Bytes: ...

    @property
    def clock_seq(self) -> Int: ...

    @property
    def clock_seq_hi_variant(self) -> Int: ...

    @property
    def clock_seq_low(self) -> Int: ...

    @property
    def fields(self) -> FieldsType: ...

    @property
    def hex(self) -> str: ...

    @property
    def int(self) -> Int: ...

    @property
    def node(self) -> Int: ...

    @property
    def time(self) -> Int: ...

    @property
    def time_hi_version(self) -> Int: ...

    @property
    def time_low(self) -> Int: ...

    @property
    def time_mid(self) -> Int: ...

    @property
    def urn(self) -> str: ...

    @property
    def variant(self) -> str: ...

    @property
    def version(self) -> str: ...

def getnode() -> Int: ...
def uuid1(node: Int=..., clock_seq: Int=...) -> UUID: ...
def uuid3(namespace: UUID, name: str) -> UUID: ...
def uuid4() -> UUID: ...
def uuid5(namespace: UUID, name: str) -> UUID: ...

NAMESPACE_DNS = ... # type: UUID
NAMESPACE_URL = ... # type: UUID
NAMESPACE_OID = ... # type: UUID
NAMESPACE_X500 = ... # type: UUID
RESERVED_NCS = ... # type: str
RFC_4122 = ... # type: str
RESERVED_MICROSOFT = ... # type: str
RESERVED_FUTURE = ... # type: str
