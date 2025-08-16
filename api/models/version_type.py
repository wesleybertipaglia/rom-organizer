from enum import Enum, auto

class VersionType(Enum):
    MAIN = auto()
    SUBSET = auto()
    PROTOTYPE = auto()
    UNLICENSED = auto()
    HACK = auto()
