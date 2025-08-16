from api.models.base import Base
from api.models.version_type import VersionType

class GameVersion(Base):
    def __init__(self, id=None, signature=None, game_title_id=None, system_id=None, region_id=None, year=None, languages=None,
                 type_=None, title=None, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)        
        self.signature = signature
        self.game_title_id = game_title_id
        self.system_id = system_id
        self.region_id = region_id
        self.year = year
        self.languages = languages
        self.type = type_
        self.title = title

    def __repr__(self):
        return f"<GameVersion id={self.id} signature={self.signature}>"

    def validate(self):        
        if not self.signature:
            raise ValueError("Signature is required")
        if not self.game_title_id:
            raise ValueError("GameTitle ID is required")
        if not self.system_id:
            raise ValueError("System ID is required")
        if not self.region_id:
            raise ValueError("Region ID is required")
        if not self.year:
            raise ValueError("Year is required")
        if not self.languages:
            raise ValueError("Languages are required")
        if not self.type:
            raise ValueError("Type is required")
        if not isinstance(self.type, VersionType):
            try:
                self.type = VersionType[self.type.upper()]
            except Exception:
                raise ValueError(f"Invalid type: {self.type}. Must be one of {[v.name for v in VersionType]}")
