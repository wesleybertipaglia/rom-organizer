from api.models.region import Region
from api.repository.base_repository import BaseRepository

class RegionRepository(BaseRepository):
    table_name = 'region'

    def _row_to_model(self, row):
        if row is None:
            return None
        return Region(*row)

    def get_by_id(self, id_):
        row = super().get_by_id(id_)
        return self._row_to_model(row)

    def list_all(self):
        rows = super().list_all()
        return [self._row_to_model(row) for row in rows]

    def create(self, region: Region):
        data = {'name': region.name}
        new_id = super().create(**data)
        region.id = new_id
        return new_id

    def update(self, region: Region):
        data = {'name': region.name}
        return super().update(region.id, **data)