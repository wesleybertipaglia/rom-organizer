from cliengine.command import Command
from cli.types import CommandType
from cli.dat import choose_dat_file
from api.missing_roms_checker import MissingRomsChecker

class CheckMissingRomsCommand(Command):
    def name(self) -> str:
        return "Check Missing ROMs from DAT"

    def type(self):
        return CommandType.GAMELIST

    def run(self, *args, **kwargs):
        dat_file = choose_dat_file()
        if not dat_file:
            return

        roms_folder = input("📁 Enter path to ROMs folder: ").strip()

        try:
            checker = MissingRomsChecker(dat_file, roms_folder)
            result = checker.run()

            print(f"\n✅ Missing ROMs list saved to: {result['output_file']}")
            print(f"📦 Total expected: {result['total_expected']}")
            print(f"📂 Found: {result['found']}")
            print(f"❗ Missing: {result['missing']}")

        except Exception as e:
            print(f"❌ Error while checking ROMs: {e}")
