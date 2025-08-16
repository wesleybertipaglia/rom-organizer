from cliengine.command import Command
from api.controllers.game_version_controller import GameVersionController
from api.models.game_version import GameVersion
from api.repository.game_version_repository import GameVersionRepository
from api.service.game_version_service import GameVersionService
from cli.types import CommandType
from api.models.version_type import VersionType

class GameVersionCommand(Command):
    def __init__(self):
        repo = GameVersionRepository()
        service = GameVersionService(repo)
        self.controller = GameVersionController(service)

    def name(self) -> str:
        return "Manage Game Versions"

    def type(self):
        return CommandType.API

    def run(self, *args, **kwargs):
        actions = {
            "1": "List all",
            "2": "Get by ID",
            "3": "Create new",
            "4": "Update existing",
            "5": "Delete by ID",
            "6": "Import from CSV"
        }

        print("\nAvailable actions:")
        for key, label in actions.items():
            print(f" {key} - {label}")

        choice = input("\nChoose an action: ").strip()

        try:
            if choice == "1":
                items = self.controller.list_all()
                if not items:
                    print("ℹ️ No game versions found.")
                for item in items:
                    print(item.__dict__)

            elif choice == "2":
                id_ = input("Enter ID: ").strip()
                result = self.controller.get(id_)
                print(result)

            elif choice == "3":
                gv = self._prompt_game_version()
                gv.validate()
                created = self.controller.create(gv)
                print("✅ Created:", created)

            elif choice == "4":
                id_ = input("Enter ID to update: ").strip()
                gv = self._prompt_game_version(id=id_)
                gv.validate()
                updated = self.controller.update(id_, gv)
                print("✅ Updated:", updated)

            elif choice == "5":
                id_ = input("Enter ID to delete: ").strip()
                self.controller.delete(id_)
                print(f"✅ Deleted GameVersion with ID {id_}")

            elif choice == "6":
                csv_path = input("Enter CSV file path: ").strip()
                result = self.controller.import_from_csv(csv_path)
                print("✅ Import result:", result)

            else:
                print("❌ Invalid option selected.")

        except Exception as e:
            print(f"❌ Error: {e}")

    def _prompt_game_version(self, id=None):
        print("Fill GameVersion fields:")

        game_title_id = input("GameTitle ID: ").strip()
        signature = input("Signature: ").strip()
        region_id = input("Region ID: ").strip()
        languages = input("Languages (comma-separated): ").strip()        
        languages_list = [lang.strip() for lang in languages.split(",")] if languages else []        
        type_str = input(f"Type (options: {[v.name for v in VersionType]}): ").strip()

        try:
            type_enum = VersionType[type_str.upper()]
        except KeyError:
            raise ValueError(f"Invalid type: {type_str}. Must be one of {[v.name for v in VersionType]}")

        title = input("Title (optional): ").strip() or None

        return GameVersion(
            id=id,
            game_title_id=game_title_id or None,
            signature=signature or None,
            region_id=region_id or None,
            languages=languages_list,
            type_=type_enum,
            title=title
        )
