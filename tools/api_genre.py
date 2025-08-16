from cliengine.command import Command
from api.controllers.genre_controller import GenreController
from api.models.genre import Genre
from api.repository.genre_repository import GenreRepository
from api.service.genre_service import GenreService
from cli.types import CommandType

class GenreApiCommand(Command):
    def __init__(self):
        repo = GenreRepository()
        service = GenreService(repo)
        self.controller = GenreController(service)

    def name(self) -> str:
        return "Manage Genres"

    def type(self):
        return CommandType.API

    def run(self, *args, **kwargs):
        actions = {
            "1": "List all",
            "2": "Get by ID",
            "3": "Create new",
            "4": "Update existing",
            "5": "Delete by ID",
            "6": "Import from CSV",
            "7": "Delete all"
        }

        print("\nAvailable actions:")
        for key, label in actions.items():
            print(f" {key} - {label}")

        choice = input("\nChoose an action: ").strip()

        try:
            if choice == "1":
                items = self.controller.list_all()
                if not items:
                    print("ℹ️ No genres found.")
                for item in items:
                    print(item.__dict__)

            elif choice == "2":
                id_ = input("Enter ID: ").strip()
                result = self.controller.get(id_)
                print(result)

            elif choice == "3":
                genre = self._prompt_genre()
                genre.validate()
                created = self.controller.create(genre)
                print("✅ Created:", created)

            elif choice == "4":
                id_ = input("Enter ID to update: ").strip()
                genre = self._prompt_genre(id=id_)
                genre.validate()
                updated = self.controller.update(id_, genre)
                print("✅ Updated:", updated)

            elif choice == "5":
                id_ = input("Enter ID to delete: ").strip()
                self.controller.delete(id_)
                print(f"✅ Deleted Genre with ID {id_}")

            elif choice == "6":
                csv_path = input("Enter CSV file path: ").strip()
                result = self.controller.import_from_csv(csv_path)
                print("✅ Import result:", result)

            elif choice == "7":
                self.controller.delete_all()
                print("✅ Deleted all Genres.")

            else:
                print("❌ Invalid option selected.")

        except Exception as e:
            print(f"❌ Error: {e}")

    def _prompt_genre(self, id=None):
        """Prompt user for Genre fields."""
        name = input("Genre name: ").strip()

        return Genre(
            id=id,
            name=name or None
        )
