from api.models.base import Base

class BaseController:
    def __init__(self, service):
        self.service = service

    def list_all(self):
        return self.service.list_all()

    def get(self, id_):
        return self.service.get_by_id(id_)

    def create(self, data: Base):
        return self.service.create(data)

    def update(self, id_, data: Base):
        return self.service.update(id_, data)

    def delete(self, id_):
        self.service.delete(id_)

    def import_from_csv(self, csv_path):
        return self.service.import_from_csv(csv_path)
    
    def delete_all(self):
        return self.service.delete_all()
