from api.models.base import Base
from api.models.version_type import VersionType

class GameVersion(Base):
    def __init__(self, id=None, game_title_id=None, signature=None, region_id=None, languages=None,
                 type_=None, title=None, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)
        self.game_title_id = game_title_id
        self.signature = signature
        self.region_id = region_id
        self.languages = languages
        self.type = type_
        self.title = title

    def __repr__(self):
        return f"<GameVersion id={self.id} signature={self.signature}>"

    def validate(self):
        if not self.game_title_id:
            raise ValueError("GameTitle ID is required")
        if not self.signature:
            raise ValueError("Signature is required")
        if not self.region_id:
            raise ValueError("Region ID is required")
        if not self.languages:
            raise ValueError("Languages are required")
        if not self.type:
            raise ValueError("Type is required")
        if not isinstance(self.type, VersionType):
            try:
                self.type = VersionType[self.type.upper()]
            except Exception:
                raise ValueError(f"Invalid type: {self.type}. Must be one of {[v.name for v in VersionType]}")
