from api.models.system import System
from api.repository.base_repository import BaseRepository

class SystemRepository(BaseRepository):
    table_name = 'system'

    def _row_to_model(self, row):
        if row is None:
            return None
        return System(*row)

    def get_by_id(self, id_):
        row = super().get_by_id(id_)
        return self._row_to_model(row)

    def list_all(self):
        rows = super().list_all()
        return [self._row_to_model(row) for row in rows]

    def create(self, system: System):
        data = {'acron': system.acron, 'name': system.name}
        new_id = super().create(**data)
        system.id = new_id
        return new_id

    def update(self, system: System):
        data = {'acron': system.acron, 'name': system.name}
        return super().update(system.id, **data)
