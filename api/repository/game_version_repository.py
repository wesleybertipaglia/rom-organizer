from api.models.game_version import GameVersion
from api.repository.base_repository import BaseRepository

class GameVersionRepository(BaseRepository):
    table_name = 'game_version'

    def _row_to_model(self, row):
        if row is None:
            return None
        return GameVersion(*row)

    def get_by_id(self, id_):
        row = super().get_by_id(id_)
        return self._row_to_model(row)

    def list_all(self):
        rows = super().list_all()
        return [self._row_to_model(row) for row in rows]

    def create(self, game_version: GameVersion):
        data = {
            'game_title_id': game_version.game_title_id,
            'signature': game_version.signature,
            'region_id': game_version.region_id,
            'languages': game_version.languages,
            'type': game_version.type,
            'title': game_version.title,
        }
        new_id = super().create(**data)
        game_version.id = new_id
        return new_id

    def update(self, game_version: GameVersion):
        data = {
            'game_title_id': game_version.game_title_id,
            'signature': game_version.signature,
            'region_id': game_version.region_id,
            'languages': game_version.languages,
            'type': game_version.type,
            'title': game_version.title,
        }
        return super().update(game_version.id, **data)
