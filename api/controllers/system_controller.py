from api.controllers.base_controller import BaseController
from api.models.system import System

class SystemController(BaseController):
    def __init__(self, service):
        super().__init__(service)

    def create(self, data: System):
        return super().create(data)

    def update(self, id_, data: System):
        return super().update(id_, data)
