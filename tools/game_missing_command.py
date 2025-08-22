from cliengine.command import Command
from api.command_type import CommandType
from api.dat_loader import choose_dat_file
from api.game_missing import MissingRomsChecker

class CheckMissingRomsCommand(Command):
    def name(self) -> str:
        return "Check Missing ROMs from DAT"

    def type(self):
        return CommandType.GAME

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
