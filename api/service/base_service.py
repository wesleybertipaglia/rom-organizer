import csv
from api.models.base import Base

class BaseService:
    def __init__(self, repository):
        self.repo = repository

    def list_all(self):
        return self.repo.list_all()

    def get_by_id(self, id_):
        entity = self.repo.get_by_id(id_)
        if not entity:
            raise ValueError(f"{self.__class__.__name__}: Entity with id {id_} not found")
        return entity

    def create(self, data: Base):
        data.validate()
        data_dict = data.__dict__.copy()
        return self.repo.create(**data_dict)

    def update(self, id_, data: Base):
        self.get_by_id(id_)
        data.validate()
        data_dict = data.__dict__.copy()
        return self.repo.update(id_, **data_dict)

    def delete(self, id_):
        self.get_by_id(id_)
        self.repo.delete(id_)

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
                    data = Base(**row)
                    data.validate()
                    self.create(data)
                    created += 1
                except Exception as e:
                    errors.append(f"Line {idx}: {e}")

        return {
            "created": created,
            "errors": errors
        }