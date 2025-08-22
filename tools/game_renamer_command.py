from cliengine.command import Command
from cli.types import CommandType
from cli.dat import choose_dat_file
from api.game_renamer import RomRenamer

class CorrectRomsNamesByDatCommand(Command):
    def name(self) -> str:
        return "Correct ROMs Names using DAT file (Copy to _corrected folder)"

    def type(self):
        return CommandType.GAME

    def run(self, *args, **kwargs):
        dat_file = choose_dat_file()
        if not dat_file:
            return

        roms_folder = input("📁 Enter path to ROMs folder: ").strip()

        try:
            renamer = RomRenamer(dat_file, roms_folder)
            result = renamer.run()

            for original, new in result["renamed_files"]:
                print(f"✔ {original} -> {new}")

            print("\n✅ Copy Summary:")
            print(f" • Copied and renamed: {result['copied']}")
            print(f" • Skipped non-files: {result['skipped']}")
            print(f" • No match: {result['unmatched']}")
            print(f"📂 Output folder: {result['output_folder']}")

        except Exception as e:
            print(f"❌ Error: {e}")
