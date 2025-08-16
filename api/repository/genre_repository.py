from api.models.genre import Genre
from api.repository.base_repository import BaseRepository

class GenreRepository(BaseRepository):
    table_name = 'genre'

    def _row_to_model(self, row):
        if row is None:
            return None
        return Genre(*row)

    def get_by_id(self, id_):
        row = super().get_by_id(id_)
        return self._row_to_model(row)

    def list_all(self):
        rows = super().list_all()
        return [self._row_to_model(row) for row in rows]

    def create(self, genre: Genre):
        data = {'name': genre.name}
        new_id = super().create(**data)
        genre.id = new_id
        return new_id

    def update(self, genre: Genre):
        data = {'name': genre.name}
        return super().update(genre.id, **data)