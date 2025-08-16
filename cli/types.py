from enum import Enum, auto

class CommandType(Enum):
    """Enum for different types of commands."""
    PIPELINE = auto()
    RENAMER = auto()
    CLEANER = auto()
    COMPRESSOR = auto()
    ART = auto()
    API = auto()
