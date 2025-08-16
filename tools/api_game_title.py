from cliengine.command import Command
from api.controllers.game_title_controller import GameTitleController
from api.models.game_title import GameTitle
from api.repository.game_title_repository import GameTitleRepository
from api.service.game_title_service import GameTitleService
from cli.types import CommandType

class GameTitleApiCommand(Command):
    def __init__(self):
        repo = GameTitleRepository()
        service = GameTitleService(repo)
        self.controller = GameTitleController(service)

    def name(self) -> str:
        return "Manage Game Titles"

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
                    print("ℹ️  No game titles found.")
                for item in items:
                    print(item.__dict__)

            elif choice == "2":
                id_ = input("Enter ID: ").strip()
                result = self.controller.get(id_)
                print(result)

            elif choice == "3":
                game_title = self._prompt_game_title()
                game_title.validate()
                created = self.controller.create(game_title)
                print("✅ Created:", created)

            elif choice == "4":
                id_ = input("Enter ID to update: ").strip()
                game_title = self._prompt_game_title(id=id_)
                game_title.validate()
                updated = self.controller.update(id_, game_title)
                print("✅ Updated:", updated)

            elif choice == "5":
                id_ = input("Enter ID to delete: ").strip()
                self.controller.delete(id_)
                print(f"✅ Deleted GameTitle with ID {id_}")

            elif choice == "6":
                csv_path = input("Enter CSV file path: ").strip()
                result = self.controller.import_from_csv(csv_path)
                print("✅ Import result:", result)

            elif choice == "7":
                self.controller.delete_all()
                print("✅ Deleted all GameTitles.")

            else:
                print("❌ Invalid option selected.")

        except Exception as e:
            print(f"❌ Error: {e}")

    def _prompt_game_title(self, id=None):
        """Prompt user to input fields for GameTitle creation or update."""
        genre_id = input("Genre ID: ").strip()
        title = input("Title: ").strip()
        synopsis = input("Synopsis (optional): ").strip()

        return GameTitle(
            id=id,
            genre_id=genre_id or None,
            title=title or None,
            synopsis=synopsis or None
        )
