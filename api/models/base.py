class Base:
    def __init__(self, id=None, created_at=None, updated_at=None):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at        

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"

    def validate(self):
        if not self.id:
            raise ValueError("ID is required")                