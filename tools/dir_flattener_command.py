from cliengine.command import Command
from api.command_type import CommandType
from api.dir_flattener import DirectoryFlattener

class FlattenDirectoryCommand(Command):
    def name(self):
        return "Flatten Directory (Move Files to Root)"

    def type(self):
        return CommandType.DIR

    def run(self, *args, **kwargs):
        path = input("Enter the root folder path: ").strip()

        try:
            flattener = DirectoryFlattener(path)
            result = flattener.flatten()

            for index, file, dst in result["move_log"]:
                print(f"{index} 📁 Moved: {file} -> {dst}")

            print(f"\n✅ Total files moved: {result['files_moved']}")

        except Exception as e:
            print(f"❌ Error: {e}")
