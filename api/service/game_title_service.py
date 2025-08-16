import csv
from api.service.base_service import BaseService
from api.models.game_title import GameTitle

class GameTitleService(BaseService):
    def create(self, data: GameTitle):
        data.validate()
        return self.repo.create(data)

    def update(self, data: GameTitle):
        data.validate()
        return self.repo.update(data.id, data)

    def import_from_csv(self, csv_path):
        created = 0
        errors = []

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for idx, row in enumerate(reader, start=1):
                row.pop('id', None)
                row.pop('created_at', None)
                row.pop('updated_at', None)

                try:
                    game_title = GameTitle(**row)
                    game_title.validate()
                    self.create(game_title)
                    created += 1
                except Exception as e:
                    errors.append(f"Line {idx}: {e}")

        return {
            "created": created,
            "errors": errors
        }