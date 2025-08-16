from api.controllers.base_controller import BaseController
from api.models.genre import Genre

class GenreController(BaseController):
    def __init__(self, service):
        super().__init__(service)

    def create(self, data: Genre):
        return super().create(data)

    def update(self, id_, data: Genre):
        return super().update(id_, data)
