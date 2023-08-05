from typing import Any, Callable, Generator, Iterable, Iterator, TypeVar, Union

from .coroutines import coroutine
from .events import AbstractEventLoop
from .futures import Future

T = TypeVar('T')

__all__ = ...  # type: str

class _ContextManager:
    def __init__(self, lock: Union[Lock, Semaphore]) -> None: ...
    def __enter__(self) -> object: ...
    def __exit__(self, *args: Any) -> None: ...

class _ContextManagerMixin(Future[_ContextManager]):
    # Apparently this exists to *prohibit* use as a context manager.
    def __enter__(self) -> object: ...
    def __exit__(self, *args: Any) -> None: ...
    def __aenter__(self): ...
    def __aexit__(self, exc_type, exc, tb): ...

class Lock(_ContextManagerMixin):
    def __init__(self, *, loop: AbstractEventLoop = None) -> None: ...
    def locked(self) -> bool: ...
    @coroutine
    def acquire(self) -> Future[bool]: ...
    def release(self) -> None: ...

class Event:
    def __init__(self, *, loop: AbstractEventLoop = None) -> None: ...
    def is_set(self) -> bool: ...
    def set(self) -> None: ...
    def clear(self) -> None: ...
    
    def wait(self) -> bool: ...

class Condition(_ContextManagerMixin):
    def __init__(self, lock: Lock = None, *, loop: AbstractEventLoop = None) -> None: ...
    def locked(self) -> bool: ...
    @coroutine
    def acquire(self) -> Future[bool]: ...
    def release(self) -> None: ...
    @coroutine
    def wait(self) -> Future[bool]: ...
    @coroutine
    def wait_for(self, predicate: Callable[[], T]) -> Future[T]: ...
    def notify(self, n: int = 1) -> None: ...
    def notify_all(self) -> None: ...

class Semaphore(_ContextManagerMixin):
    def __init__(self, value: int = 1, *, loop: AbstractEventLoop = None) -> None: ...
    def locked(self) -> bool: ...
    @coroutine
    def acquire(self) -> Future[bool]: ...
    def release(self) -> None: ...

class BoundedSemaphore(Semaphore):
    def __init__(self, value=1, *, loop: AbstractEventLoop = None) -> None: ...
