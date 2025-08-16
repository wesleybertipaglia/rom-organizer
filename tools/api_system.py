from cliengine.command import Command
from api.controllers.system_controller import SystemController
from api.models.system import System
from api.repository.system_repository import SystemRepository
from api.service.system_service import SystemService
from cli.types import CommandType

class SystemApiCommand(Command):
    def __init__(self):
        repo = SystemRepository()
        service = SystemService(repo)
        self.controller = SystemController(service)

    def name(self) -> str:
        return "Manage Systems"

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
                    print("ℹ️  No systems found.")
                for item in items:
                    print(item.__dict__)

            elif choice == "2":
                id_ = input("Enter ID: ").strip()
                result = self.controller.get(id_)
                print(result)

            elif choice == "3":
                system = self._prompt_system()
                system.validate()
                created = self.controller.create(system)
                print("✅ Created:", created)

            elif choice == "4":
                id_ = input("Enter ID to update: ").strip()
                system = self._prompt_system(id=id_)
                system.validate()
                updated = self.controller.update(id_, system)
                print("✅ Updated:", updated)

            elif choice == "5":
                id_ = input("Enter ID to delete: ").strip()
                self.controller.delete(id_)
                print(f"✅ Deleted System with ID {id_}")

            elif choice == "6":
                csv_path = input("Enter CSV file path: ").strip()
                result = self.controller.import_from_csv(csv_path)
                print("✅ Import result:", result)

            else:
                print("❌ Invalid option selected.")

        except Exception as e:
            print(f"❌ Error: {e}")

    def _prompt_system(self, id=None):
        """Prompt user for System fields."""
        name = input("System name: ").strip()

        return System(
            id=id,
            name=name or None
        )
