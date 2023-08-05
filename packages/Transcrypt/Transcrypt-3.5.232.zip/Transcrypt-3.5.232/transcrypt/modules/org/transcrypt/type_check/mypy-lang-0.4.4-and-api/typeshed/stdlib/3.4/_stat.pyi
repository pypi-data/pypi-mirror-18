"""Stub file for the '_stat' module."""

SF_APPEND = ...  # type: int
SF_ARCHIVED = ...  # type: int
SF_IMMUTABLE = ...  # type: int
SF_NOUNLINK = ...  # type: int
SF_SNAPSHOT = ...  # type: int
ST_ATIME = ...  # type: int
ST_CTIME = ...  # type: int
ST_DEV = ...  # type: int
ST_GID = ...  # type: int
ST_INO = ...  # type: int
ST_MODE = ...  # type: int
ST_MTIME = ...  # type: int
ST_NLINK = ...  # type: int
ST_SIZE = ...  # type: int
ST_UID = ...  # type: int
S_ENFMT = ...  # type: int
S_IEXEC = ...  # type: int
S_IFBLK = ...  # type: int
S_IFCHR = ...  # type: int
S_IFDIR = ...  # type: int
S_IFDOOR = ...  # type: int
S_IFIFO = ...  # type: int
S_IFLNK = ...  # type: int
S_IFPORT = ...  # type: int
S_IFREG = ...  # type: int
S_IFSOCK = ...  # type: int
S_IFWHT = ...  # type: int
S_IREAD = ...  # type: int
S_IRGRP = ...  # type: int
S_IROTH = ...  # type: int
S_IRUSR = ...  # type: int
S_IRWXG = ...  # type: int
S_IRWXO = ...  # type: int
S_IRWXU = ...  # type: int
S_ISGID = ...  # type: int
S_ISUID = ...  # type: int
S_ISVTX = ...  # type: int
S_IWGRP = ...  # type: int
S_IWOTH = ...  # type: int
S_IWRITE = ...  # type: int
S_IWUSR = ...  # type: int
S_IXGRP = ...  # type: int
S_IXOTH = ...  # type: int
S_IXUSR = ...  # type: int
UF_APPEND = ...  # type: int
UF_COMPRESSED = ...  # type: int
UF_HIDDEN = ...  # type: int
UF_IMMUTABLE = ...  # type: int
UF_NODUMP = ...  # type: int
UF_NOUNLINK = ...  # type: int
UF_OPAQUE = ...  # type: int

def S_IMODE(mode: int) -> int: ...
def S_IFMT(mode: int) -> int: ...

def S_ISBLK(mode: int) -> bool: ...
def S_ISCHR(mode: int) -> bool: ...
def S_ISDIR(mode: int) -> bool: ...
def S_ISDOOR(mode: int) -> bool: ...
def S_ISFIFO(mode: int ) -> bool: ...
def S_ISLNK(mode: int) -> bool: ...
def S_ISPORT(mode: int) -> bool: ...
def S_ISREG(mode: int) -> bool: ...
def S_ISSOCK(mode: int) -> bool: ...
def S_ISWHT(mode: int) -> bool: ...

def filemode(mode: int) -> str: ...
