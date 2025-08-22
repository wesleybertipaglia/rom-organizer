from enum import Enum, auto

class CommandType(Enum):
    """Enum for different types of commands."""
    PIPELINE = auto()
    GAME = auto()
    FILE = auto()
    DIR = auto()
