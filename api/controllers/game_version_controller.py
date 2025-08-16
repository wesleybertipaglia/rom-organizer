from api.controllers.base_controller import BaseController
from api.models.game_version import GameVersion

class GameVersionController(BaseController):
    def __init__(self, service):
        super().__init__(service)

    def create(self, data: GameVersion):
        return super().create(data)

    def update(self, id_, data: GameVersion):
        return super().update(id_, data)
