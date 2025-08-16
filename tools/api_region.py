from cliengine.command import Command
from api.controllers.region_controller import RegionController
from api.models.region import Region
from api.repository.region_repository import RegionRepository
from api.service.region_service import RegionService
from cli.types import CommandType

class RegionApiCommand(Command):
    def __init__(self):
        repo = RegionRepository()
        service = RegionService(repo)
        self.controller = RegionController(service)

    def name(self) -> str:
        return "Manage Regions"

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
                    print("ℹ️  No regions found.")
                for item in items:
                    print(item.__dict__)

            elif choice == "2":
                id_ = input("Enter ID: ").strip()
                result = self.controller.get(id_)
                print(result)

            elif choice == "3":
                region = self._prompt_region()
                region.validate()
                created = self.controller.create(region)
                print("✅ Created:", created)

            elif choice == "4":
                id_ = input("Enter ID to update: ").strip()
                region = self._prompt_region(id=id_)
                region.validate()
                updated = self.controller.update(id_, region)
                print("✅ Updated:", updated)

            elif choice == "5":
                id_ = input("Enter ID to delete: ").strip()
                self.controller.delete(id_)
                print(f"✅ Deleted Region with ID {id_}")

            elif choice == "6":
                csv_path = input("Enter CSV file path: ").strip()
                result = self.controller.import_from_csv(csv_path)
                print("✅ Import result:", result)

            else:
                print("❌ Invalid option selected.")

        except Exception as e:
            print(f"❌ Error: {e}")

    def _prompt_region(self, id=None):
        """Prompt user for Region fields."""
        name = input("Region name: ").strip()

        return Region(
            id=id,
            name=name or None
        )
