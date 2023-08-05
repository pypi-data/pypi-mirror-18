# Stubs for base64

# Based on http://docs.python.org/3.2/library/base64.html

from typing import IO

def b64encode(s: str, altchars: str = ...) -> str: ...
def b64decode(s: str, altchars: str = ...,
              validate: bool = ...) -> str: ...
def standard_b64encode(s: str) -> str: ...
def standard_b64decode(s: str) -> str: ...
def urlsafe_b64encode(s: str) -> str: ...
def urlsafe_b64decode(s: str) -> str: ...
def b32encode(s: str) -> str: ...
def b32decode(s: str, casefold: bool = ...,
              map01: str = ...) -> str: ...
def b16encode(s: str) -> str: ...
def b16decode(s: str, casefold: bool = ...) -> str: ...

def decode(input: IO[str], output: IO[str]) -> None: ...
def decodebytes(s: str) -> str: ...
def decodestring(s: str) -> str: ...
def encode(input: IO[str], output: IO[str]) -> None: ...
def encodebytes(s: str) -> str: ...
def encodestring(s: str) -> str: ...
