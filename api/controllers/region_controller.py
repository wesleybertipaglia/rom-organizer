from api.controllers.base_controller import BaseController
from api.models.region import Region

class RegionController(BaseController):
    def __init__(self, service):
        super().__init__(service)

    def create(self, data: Region):
        return super().create(data)

    def update(self, id_, data: Region):
        return super().update(id_, data)
