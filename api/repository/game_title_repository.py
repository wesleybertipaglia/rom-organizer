from api.models.game_title import GameTitle
from api.repository.base_repository import BaseRepository

class GameTitleRepository(BaseRepository):
    table_name = 'game_title'

    def _row_to_model(self, row):
        if row is None:
            return None
        return GameTitle(*row)

    def get_by_id(self, id_):
        row = super().get_by_id(id_)
        return self._row_to_model(row)

    def list_all(self):
        rows = super().list_all()
        return [self._row_to_model(row) for row in rows]

    def create(self, game_title: GameTitle):
        data = {
            'system_id': game_title.system_id,
            'year': game_title.year,
            'title': game_title.title,
            'synopsis': game_title.synopsis,
            'genre_id': game_title.genre_id,
        }
        new_id = super().create(**data)
        game_title.id = new_id
        return new_id

    def update(self, game_title: GameTitle):
        data = {
            'system_id': game_title.system_id,
            'year': game_title.year,
            'title': game_title.title,
            'synopsis': game_title.synopsis,
            'genre_id': game_title.genre_id,
        }
        return super().update(game_title.id, **data)
