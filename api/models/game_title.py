from api.models.base import Base

class GameTitle(Base):
    def __init__(self, id=None, system_id=None, year=None, title=None, synopsis=None, genre_id=None, 
                 created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)
        self.system_id = system_id
        self.year = year
        self.title = title
        self.synopsis = synopsis
        self.genre_id = genre_id

    def __repr__(self):
        return f"<GameTitle id={self.id} title={self.title}>"

    def validate(self):
        if not self.title:
            raise ValueError("Title is required")
        if not self.system_id:
            raise ValueError("System ID is required")
        if not self.genre_id:
            raise ValueError("Genre ID is required")
