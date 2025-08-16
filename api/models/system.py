from api.models.base import Base

class System(Base):
    def __init__(self, id=None, name=None, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)
        self.name = name

    def __repr__(self):
        return f"<System id={self.id} name={self.name}>"

    def validate(self):
        if not self.name:
            raise ValueError("Name is required")
        if len(self.name) > 100:
            raise ValueError("Name must be 100 characters or less")
