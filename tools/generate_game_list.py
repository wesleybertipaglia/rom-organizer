from cliengine.command import Command
from cli.types import CommandType
from api.gamelist_generator import GamelistGenerator

class GenerateGamelistCommand(Command):
    def name(self) -> str:
        return "Generate Gamelist XML"

    def type(self):
        return CommandType.GAMELIST

    def run(self, *args, **kwargs):
        roms_dir = input("📁 Enter ROMs folder path: ").strip()

        try:
            generator = GamelistGenerator(roms_dir)
            output_path = generator.generate()
            print(f"✅ gamelist.xml generated successfully at: {output_path}")

        except Exception as e:
            print(f"❌ Error generating gamelist: {e}")
