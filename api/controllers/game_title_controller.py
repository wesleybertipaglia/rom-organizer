from api.controllers.base_controller import BaseController
from api.models.game_title import GameTitle

class GameTitleController(BaseController):
    def __init__(self, service):
        super().__init__(service)

    def create(self, data: GameTitle):
        return super().create(data)
    
    def update(self, id_, data: GameTitle):
        return super().update(id_, data)
